import matplotlib

matplotlib.use("Agg")  # GUI 백엔드 대신 이미지 저장용 백엔드 사용!

from datetime import datetime, time
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from django.core.files.base import ContentFile
from django.utils import timezone

from transaction.models import Transaction

from .models import Analysis


class Analyzer:
    def __init__(self, user, type, start_date, end_date):
        self.user = user
        self.type = type  # "WEEKLY" or "MONTHLY"
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        from django.utils.timezone import make_aware

        start = make_aware(datetime.combine(self.start_date, time.min))
        end = make_aware(datetime.combine(self.end_date, time.max))

        # 1. 거래 데이터 필터링
        transactions = Transaction.objects.filter(
            account__user=self.user, transaction_at__range=(start, end)
        )

        if not transactions.exists():
            return None

        # 2. Pandas DataFrame 생성
        data = pd.DataFrame(
            list(transactions.values("transaction_at", "amount", "description"))
        )

        data["transaction_at"] = pd.to_datetime(data["transaction_at"])
        data["date"] = data["transaction_at"].dt.date

        # amount 컬럼을 float으로 변환
        data["amount"] = pd.to_numeric(data["amount"], errors="coerce")

        # NaN 제거 (혹시라도 변환 실패한 값이 있을 경우)
        data = data.dropna(subset=["amount"])

        # 일자별 합계 계산
        summary = data.groupby("date")["amount"].sum()

        # 3. 시각화
        plt.figure(figsize=(10, 5))
        summary.plot(kind="bar")
        plt.title(f"{self.user.email}의 {self.type} 소비 분석")
        plt.xlabel("날짜")
        plt.ylabel("총 소비 금액")
        plt.tight_layout()

        # 4. 이미지 저장 (in-memory)
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_file = ContentFile(
            buffer.read(), name=f"{self.user.id}_{self.type.lower()}_analysis.png"
        )
        buffer.close()
        plt.close()

        # 5. Analysis 모델 저장
        analysis = Analysis.objects.create(
            user=self.user,
            about="총 지출",
            type=self.type,
            period_start=self.start_date,
            period_end=self.end_date,
            description="해당 기간 동안의 총 소비 내역",
            result_image=image_file,
        )

        return analysis
