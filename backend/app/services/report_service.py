from app.services.ranking_service import RankingService
from app.services.jd_service import JDService


class ReportService:
    def __init__(self):
        self.ranking_service = RankingService()
        self.jd_service = JDService()

    def generate_report(self, jd_text: str, top_k: int = 5) -> dict:
        jd_analysis = self.jd_service.analyze(jd_text)
        ranking = self.ranking_service.rank(jd_text, top_k=top_k)

        return {
            "jd_analysis": jd_analysis,
            "candidate_evaluations": ranking.evaluations,
        }