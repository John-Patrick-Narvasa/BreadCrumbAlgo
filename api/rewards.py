class ProgressEngine:
    def calculate_xp(self, minutes: int, is_pomodoro: bool) -> int:
        return (minutes * 10) + (50 if is_pomodoro else 0)

    def get_dashboard_state(self, total_points: int): # 3. ADDED
        level_threshold = 1000
        return (total_points % level_threshold) / level_threshold * 100