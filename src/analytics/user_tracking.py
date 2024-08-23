import os
import json
import logging
from datetime import datetime

class UserTracking:
    def __init__(self, log_dir='logs', log_file='user_tracking.log', analytics_file='user_analytics.json'):
        """
        Initialize the UserTracking system.

        :param log_dir: Directory where logs and analytics files will be stored.
        :param log_file: Log file name for tracking user interactions.
        :param analytics_file: JSON file name for storing aggregated user analytics.
        """
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        self.analytics_file = os.path.join(log_dir, analytics_file)
        os.makedirs(log_dir, exist_ok=True)
        self._setup_logging()
        self.analytics_data = self._load_analytics_data()

    def _setup_logging(self):
        """
        Set up logging for user tracking.
        """
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("UserTracking system initialized")

    def _load_analytics_data(self):
        """
        Load existing analytics data from a JSON file, or create a new one if it doesn't exist.
        """
        if os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def _save_analytics_data(self):
        """
        Save the current analytics data to a JSON file.
        """
        with open(self.analytics_file, 'w') as f:
            json.dump(self.analytics_data, f, indent=4)
        logging.info(f"Analytics data saved to {self.analytics_file}")

    def track_event(self, user_id, event_name, event_data=None):
        """
        Track a user event.

        :param user_id: Unique identifier for the user.
        :param event_name: Name of the event being tracked (e.g., 'page_view', 'click', 'purchase').
        :param event_data: Optional dictionary containing additional event data.
        """
        event_data = event_data or {}
        event_record = {
            'user_id': user_id,
            'event_name': event_name,
            'event_data': event_data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        logging.info(f"Tracked event: {event_record}")
        self._update_analytics(user_id, event_name)

    def _update_analytics(self, user_id, event_name):
        """
        Update the aggregated analytics data based on the tracked event.

        :param user_id: Unique identifier for the user.
        :param event_name: Name of the event being tracked.
        """
        if user_id not in self.analytics_data:
            self.analytics_data[user_id] = {}

        if event_name not in self.analytics_data[user_id]:
            self.analytics_data[user_id][event_name] = 0
        
        self.analytics_data[user_id][event_name] += 1
        logging.info(f"Updated analytics for user {user_id}: {self.analytics_data[user_id]}")
        self._save_analytics_data()

    def get_user_summary(self, user_id):
        """
        Retrieve a summary of all events tracked for a specific user.

        :param user_id: Unique identifier for the user.
        :return: Dictionary summarizing the user's tracked events.
        """
        return self.analytics_data.get(user_id, {})

    def get_event_summary(self, event_name):
        """
        Retrieve a summary of how many times an event has been tracked across all users.

        :param event_name: Name of the event.
        :return: Total count of the event across all users.
        """
        total_count = sum(user_data.get(event_name, 0) for user_data in self.analytics_data.values())
        return {event_name: total_count}

    def get_all_users_summary(self):
        """
        Retrieve a summary of all users and their tracked events.

        :return: Dictionary summarizing all users' tracked events.
        """
        return self.analytics_data

    def delete_user_data(self, user_id):
        """
        Delete all tracking data for a specific user.

        :param user_id: Unique identifier for the user.
        """
        if user_id in self.analytics_data:
            del self.analytics_data[user_id]
            logging.info(f"Deleted analytics data for user {user_id}")
            self._save_analytics_data()
        else:
            logging.warning(f"Attempted to delete data for non-existent user {user_id}")

    def reset_analytics(self):
        """
        Reset all analytics data.
        """
        self.analytics_data = {}
        self._save_analytics_data()
        logging.info("All analytics data has been reset")


# Example usage
if __name__ == "__main__":
    tracker = UserTracking()

    # Track some events
    tracker.track_event('user_001', 'page_view', {'page': 'home'})
    tracker.track_event('user_001', 'click', {'button': 'signup'})
    tracker.track_event('user_002', 'page_view', {'page': 'about'})
    tracker.track_event('user_002', 'purchase', {'item': 'book', 'price': 19.99})

    # Get summaries
    print("User 001 Summary:", tracker.get_user_summary('user_001'))
    print("User 002 Summary:", tracker.get_user_summary('user_002'))
    print("Page View Summary:", tracker.get_event_summary('page_view'))
    print("All Users Summary:", tracker.get_all_users_summary())

    # Delete data for a specific user
    tracker.delete_user_data('user_001')

    # Reset all analytics
    tracker.reset_analytics()
