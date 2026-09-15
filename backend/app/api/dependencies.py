from functools import lru_cache

from app.services.jd_service import JDService
from app.services.ranking_service import RankingService
from app.services.report_service import ReportService
from app.services.stats_service import StatsService


@lru_cache(maxsize=1)
def get_jd_service() -> JDService:
    return JDService()


@lru_cache(maxsize=1)
def get_ranking_service() -> RankingService:
    return RankingService()


@lru_cache(maxsize=1)
def get_report_service() -> ReportService:
    return ReportService()


@lru_cache(maxsize=1)
def get_stats_service() -> StatsService:
    return StatsService()
