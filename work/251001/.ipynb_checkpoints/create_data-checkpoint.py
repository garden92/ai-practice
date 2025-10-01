import pandas as pd
import numpy as np

class create_data:
    def __init__(self):
        self.channels = ["Email", "SMS", "Push", "Ads", "Search"]
        self.segments = ["New", "Returning"]
        self.devices = ["Mobile", "Desktop"]
        self.regions = ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju"]

    # =========================
    # 날짜 축 생성 + 시즌성/추세 함수
    # =========================

    def weekly_seasonality(self, d):  # 요일 효과 (토/일 약간 하락)
        wd = d.weekday()  # Mon=0 ... Sun=6
        return {0: 1.00, 1: 1.02, 2: 1.03, 3: 1.02, 4: 1.05, 5: 0.92, 6: 0.90}[wd]

    def monthly_seasonality(self, d):  # 월 효과 (예시)
        m = d.month
        return {1: 0.95, 2: 0.97, 3: 1.02, 4: 1.05, 5: 1.08, 6: 1.10}.get(m, 1.0)

    def linear_trend(self, dates, d):  # 초반 1.0 → 후반 1.15 정도로 증가
        t = (d - dates[0]).days / max(1, (dates[-1] - dates[0]).days)
        return 1.0 + 0.15 * t

    def catdata(self, output="output.csv"):
        np.random.seed(7)
        n = 600
        dates = pd.date_range("2024-04-01", periods=120, freq="D")
        df = pd.DataFrame({
            "date": np.random.choice(dates, size=n),
            "channel": np.random.choice(self.channels, p=[0.22, 0.18, 0.20, 0.22, 0.18], size=n),
            "segment": np.random.choice(self.segments, p=[0.55, 0.45], size=n),
            "device": np.random.choice(self.devices, p=[0.7, 0.3], size=n),
            "region": np.random.choice(self.regions, p=[0.42, 0.16, 0.14, 0.10, 0.09, 0.09], size=n),
            "response": np.random.choice(["Yes", "No"], p=[0.32, 0.68], size=n),
        })

        df.to_csv(output)

        return df

    def tmsdata(self, output="output.csv"):
        seed = 42
        start = "2024-01-01"  # 시작일
        end = "2024-06-30"  # 종료일

        base_impr = {"Ads": 5200, "Search": 4800, "Email": 1200, "SMS": 1100, "Push": 1300}
        p_click = {"Ads": 0.030, "Search": 0.050, "Email": 0.090, "SMS": 0.085, "Push": 0.080}
        cpi = {"Ads": 0.015, "Search": 0.010, "Email": 0.003, "SMS": 0.003, "Push": 0.003}

        # 세그먼트별 전환율(클릭→전환)
        p_conv = {"New": 0.060, "Returning": 0.080}
        # 디바이스/지역 비율(선호도)
        device_p = [0.6, 0.4]  # Mobile, Desktop
        region_p = [0.35, 0.15, 0.2, 0.1, 0.1, 0.1]
        np.random.seed(seed)
        dates = pd.date_range(start, end, freq="D")

        rows = []
        for d in dates:
            w = self.weekly_seasonality(d)
            m = self.monthly_seasonality(d)
            tr = self.linear_trend(dates, d)
            for ch in self.channels:
                for seg in self.segments:
                    # 기본 임프 × (요일·월·추세) × 노이즈
                    lam = base_impr[ch] * w * m * tr
                    impressions = np.random.poisson(max(1, lam))

                    # 클릭: 임프 × CTR (채널별)
                    clicks = np.random.binomial(impressions, p_click[ch]) if impressions > 0 else 0

                    # 비용: 임프 × cpi
                    cost = impressions * cpi[ch]

                    # 전환: 클릭 × CVR (세그먼트별)
                    conversions = np.random.binomial(clicks, p_conv[seg]) if clicks > 0 else 0

                    # 매출: 전환 × 객단가(랜덤)
                    # Returning 고객이 약간 높은 객단가
                    arpu = np.random.uniform(20, 60) * (1.05 if seg == "Returning" else 1.0)
                    revenue = conversions * arpu

                    device = np.random.choice(self.devices, p=device_p)
                    region = np.random.choice(self.regions, p=region_p)
                    campaign = f"{ch[:2].upper()}-{np.random.randint(1, 8)}"

                    rows.append([
                        d.date(), ch, campaign, seg, device, region,
                        impressions, clicks, round(cost, 2), conversions, round(revenue, 2)
                    ])

        df = pd.DataFrame(rows, columns=[
            "date", "channel", "campaign", "segment", "device", "region",
            "impressions", "clicks", "cost", "conversions", "revenue"
        ])

        # 파생지표
        df["ctr"] = (df["clicks"] / df["impressions"]).replace([np.inf, -np.inf], 0).fillna(0)
        df["cvr"] = (df["conversions"] / df["clicks"]).replace([np.inf, -np.inf], 0).fillna(0)
        df["cpc"] = (df["cost"] / df["clicks"]).replace([np.inf, -np.inf], 0).fillna(0)
        df["cac"] = (df["cost"] / df["conversions"]).replace([np.inf, -np.inf], 0).fillna(0)
        df["roas"] = (df["revenue"] / df["cost"]).replace([np.inf, -np.inf], 0).fillna(0)

        df.to_csv(output)

        return df