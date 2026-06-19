import pytest
import uuid
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch, MagicMock

from app.models.carbon import CarbonFootprint
from app.models.extras import SustainabilityReport
from app.services.report_service import report_service

@pytest.mark.anyio
async def test_generate_weekly_report_no_footprints():
    # If no footprints exist, it should return None
    db_mock = AsyncMock()
    result_mock = MagicMock()
    result_mock.scalars().all.return_value = []
    db_mock.execute.return_value = result_mock

    user_id = uuid.uuid4()
    report = await report_service.generate_weekly_report(db_mock, user_id)
    assert report is None

@pytest.mark.anyio
@patch("app.services.report_service.get_anthropic_client")
async def test_generate_weekly_report_success(mock_get_client):
    db_mock = AsyncMock()
    
    # Mock footprints
    fp1 = CarbonFootprint(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        monthly_kg=400.0,
        grade="GOOD",
        breakdown={},
        ai_sustainability_score=75,
        created_at=date.today()
    )
    fp2 = CarbonFootprint(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        monthly_kg=450.0,
        grade="MODERATE",
        breakdown={},
        ai_sustainability_score=60,
        created_at=date.today() - timedelta(days=5)
    )
    
    result_mock = MagicMock()
    result_mock.scalars().all.return_value = [fp1, fp2]
    db_mock.execute.return_value = result_mock
    
    # Mock Anthropic Response
    mock_client = AsyncMock()
    mock_get_client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='{"summary_text": "Great job reducing emissions!", "key_insights": [{"text": "Reduced energy usage", "metric": "-50kg"}]}')]
    mock_client.messages.create.return_value = mock_response
    
    user_id = uuid.uuid4()
    report = await report_service.generate_weekly_report(db_mock, user_id)
    
    assert report is not None
    assert report.summary_text == "Great job reducing emissions!"
    assert len(report.key_insights) == 1
    assert report.key_insights[0]["metric"] == "-50kg"
    assert report.carbon_saved_kg == 50.0
    assert report.ai_sustainability_score == 75

@pytest.mark.anyio
async def test_get_user_reports():
    db_mock = AsyncMock()
    user_id = uuid.uuid4()
    
    mock_report = SustainabilityReport(
        id=uuid.uuid4(),
        user_id=user_id,
        summary_text="Report summary",
        key_insights=[]
    )
    
    result_mock = MagicMock()
    result_mock.scalars().all.return_value = [mock_report]
    db_mock.execute.return_value = result_mock
    
    reports = await report_service.get_user_reports(db_mock, user_id)
    assert len(reports) == 1
    assert reports[0].summary_text == "Report summary"
