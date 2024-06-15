from datetime import datetime, timedelta

def default_dates(request):
    return {
        'default_start_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        'default_end_date': datetime.now().strftime('%Y-%m-%d'),
        'default_specific_date': '',  # or set a default specific date if needed
    }
