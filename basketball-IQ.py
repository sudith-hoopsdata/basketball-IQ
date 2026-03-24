import sys
import cv2
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, QGridLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoScoutTracker(QWidget):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print(f"❌ Error: Could not open {self.video_path}.")
            sys.exit()
            
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        
        self.player_scores = {} 
        self.event_log = []
        self.is_paused = False
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Automated Basketball Scout Tracker (Master Rubric)')
        
        main_layout = QHBoxLayout()
        video_layout = QVBoxLayout()
        
        # --- NEW: We use a Grid Layout for the buttons so they all fit! ---
        right_panel_layout = QVBoxLayout()
        button_grid = QGridLayout() 
        
        # The Video Screen
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(800, 450)
        self.video_label.setStyleSheet("background-color: black;")
        video_layout.addWidget(self.video_label)
        
        help_text = QLabel("Controls: [Space] Play/Pause | [Right] Skip +10s | [Left] Rewind -10s", self)
        help_text.setStyleSheet("font-size: 14px; font-style: italic; color: gray;")
        video_layout.addWidget(help_text)
        
        self.leaderboard_label = QLabel("Player IQ Scores:\nNo data yet...", self)
        self.leaderboard_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px; color: blue;")
        right_panel_layout.addWidget(self.leaderboard_label)
        
        self.btn_pause = QPushButton("⏯ Play / Pause (Spacebar)", self)
        self.btn_pause.setStyleSheet("background-color: #d3d3d3; font-size: 14px; padding: 10px; margin-bottom: 10px;")
        self.btn_pause.clicked.connect(self.toggle_pause)
        right_panel_layout.addWidget(self.btn_pause)
        
        # ==========================================
        # 🏀  MASTER RUBRIC FROM THE SPREADSHEET
        # ==========================================
        self.scoring_key = {
            # Playmaking / Passing
            'P&R Drop (Right Decision)': 2.0,
            'P&R Drop (Incorrect Decision)': -2.0,
            'Screen Assist (Make)': 2.0,
            'Screen Assist (Open Miss)': 1.0,
            'Screen Assist (Contested)': -2.0,
            'Fake Assist (Make)': 1.0,
            'Fake Assist (Miss)': 0.0,
            'Pass: >35% 3PT Shooter': 2.0,
            'Pass: <35% 3PT Shooter': -1.0,
            'Pass: <10s into shot clock': 2.0,
            'Pass: <5s left on clock': -1.0,
            'Pass: Corner 3PT': 1.0,
            'Pass: Close Shot': 2.0,
            
            # Defense
            'Def Mismatch: Small on Big (Stop)': 2.0,
            'Def Mismatch: Small on Big (Made)': -1.0,
            'Def: Force Pickup @ 3PT Line': 2.0,
            'Def: Force Pickup @ FT Line': 1.0,
            
            # Ball Handling
            'BH: Beats FCP': 2.0,
            'BH: Forced Turnover': -1.0,
            'BH: Unforced Turnover': -2.0,
            
            # Shooting
            'Shoot: Mid-Range (Make)': 0.5,
            'Shoot: Mid-Range (Miss)': -2.0,
            'Shoot >35%: Open': 2.0,
            'Shoot >35%: Contested': -1.0,
            'Shoot <35%: Open': 1.0,
            'Shoot <35%: Contested': -2.0,
            'Grenade <4s (Make)': 2.0,
            'Grenade <4s (Miss)': 0.0
        }
        
        # Populate the 2-column Grid Layout
        row = 0
        col = 0
        for event_name, points in self.scoring_key.items():
            btn = QPushButton(f"{event_name} ({points})", self)
            
            # Dynamic colors based on point values
            if points > 0: color = "#98fb98" # Green
            elif points < 0: color = "#ffcccb" # Red
            else: color = "#e0e0e0" # Gray for 0 points
                
            btn.setStyleSheet(f"background-color: {color}; font-size: 11px; padding: 5px;")
            btn.clicked.connect(lambda checked, e=event_name, p=points: self.log_event(e, p))
            
            button_grid.addWidget(btn, row, col)
            col += 1
            if col > 1: # Move to next row after 2 columns
                col = 0
                row += 1
                
        right_panel_layout.addLayout(button_grid)
            
        self.btn_export = QPushButton("💾 Export CSV & Exit", self)
        self.btn_export.setStyleSheet("background-color: black; color: white; font-size: 14px; font-weight: bold; padding: 10px; margin-top: 10px;")
        self.btn_export.clicked.connect(self.export_and_quit)
        right_panel_layout.addWidget(self.btn_export)
        
        main_layout.addLayout(video_layout)
        main_layout.addLayout(right_panel_layout)
        self.setLayout(main_layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1000 / self.fps))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.toggle_pause()
        elif event.key() == Qt.Key_Right:
            self.skip_video(10)  
        elif event.key() == Qt.Key_Left:
            self.skip_video(-10) 

    def skip_video(self, seconds):
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        target_frame = max(0, min(current_frame + (seconds * self.fps), self.total_frames - 1))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        if self.is_paused:
            ret, frame = self.cap.read()
            if ret:
                self.display_frame(frame)

    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.timer.start(int(1000 / self.fps))
        else:
            self.is_paused = True
            self.timer.stop()
            
    def log_event(self, event_name, points):
        was_playing = not self.is_paused
        if was_playing:
            self.toggle_pause()
            
        player_input, ok = QInputDialog.getText(self, "Tag Player(s)", f"Action: {event_name}\nEnter Jersey #(s) separated by commas:")
        
        if ok and player_input:
            players = [p.strip() for p in player_input.split(',')]
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            timestamp = round(current_frame / self.fps, 2)
            
            for player_id in players:
                if not player_id: 
                    continue 
                    
                if player_id not in self.player_scores:
                    self.player_scores[player_id] = 0.0
                    
                self.player_scores[player_id] += points
                
                self.event_log.append({
                    'Time (sec)': timestamp,
                    'Player': player_id,
                    'Event': event_name,
                    'Points Awarded': points,
                    'Player Total IQ': self.player_scores[player_id]
                })
                print(f"✅ Logged: Player {player_id} | {event_name} | Added: {points}")
            
            leaderboard_text = "Player IQ Scores:\n"
            sorted_players = sorted(self.player_scores.items(), key=lambda item: item[1], reverse=True)
            for pid, pscore in sorted_players:
                leaderboard_text += f"Player {pid}: {pscore} pts\n"
            self.leaderboard_label.setText(leaderboard_text)
        
        if was_playing:
            self.toggle_pause()
            
    def display_frame(self, frame):
        frame = cv2.resize(frame, (800, 450))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.display_frame(frame)
        else:
            self.timer.stop()
            print("\nVideo ended.")
            
    def export_and_quit(self):
        if self.event_log:
            df = pd.DataFrame(self.event_log)
            df.to_csv('scouting_report.csv', index=False)
            print("\n✅ Success! Data saved to 'scouting_report.csv'")
        self.cap.release()
        self.close()

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        
    tracker = VideoScoutTracker("/Users/sudithmarti/UConn vs. Purdue - 2024 NCAA men's national championship ｜ FULL REPLAY [M4N2eDKekIg].webm")
    tracker.show()
    app.exec_()