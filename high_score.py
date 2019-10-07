from pygame.font import Font


class HighScore:
    def __init__(self, file_name, game_settings, game_stats, screen):
        self.fname = file_name
        self.settings = game_settings
        self.stats = game_stats
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = Font(None, 32)
        self.text_color = (255, 255, 255)
        self.data = []

        try:
            with open(self.fname, "r") as f:
                score = f.read().split()
                for i in range(len(score)):
                    self.data.append(int(score[i]))
            f.close()
            if len(self.data) > 0:
                self.data.sort(reverse=True)
                n = 10 if (len(self.data) > 10) else len(self.data)
                self.data = self.data[:n]
                self.stats.high_score = self.data[0]
            else:
                self.stats.high_score = 0
        except IOError:
            print("Save file not found.")
            self.stats.high_score = 0
        except ValueError:
            self.data.clear()
            self.stats.high_score = 0

        # High score screen
        self.score_text = self.font.render("SCORE", True, self.text_color, self.settings.bg_color)
        self.score_text_rect = self.score_text.get_rect()
        self.score_text_rect.right = self.screen_rect.centerx + 50
        self.score_text_rect.top = 50
        self.rank_text = self.font.render("RANK", True, self.text_color, self.settings.bg_color)
        self.rank_text_rect = self.rank_text.get_rect()
        self.rank_text_rect.top = self.score_text_rect.top
        self.rank_text_rect.right = self.screen_rect.centerx / 2
        self.table = []
        self.prep_score_table()

    def prep_score_table(self):
        for i in range(len(self.data)):
            number = self.font.render(str(i + 1), True, self.text_color, self.settings.bg_color)
            number_rect = number.get_rect()
            number_rect.right = self.rank_text_rect.right
            number_rect.y = self.score_text_rect.bottom + 20 * (i + 1)
            score = self.font.render((str(self.data[i])), True, self.text_color, self.settings.bg_color)
            score_rect = score.get_rect()
            score_rect.right = self.score_text_rect.right
            score_rect.y = number_rect.y
            record = [number, number_rect, score, score_rect]
            self.table.append(record)

    def save(self):
        with open(self.fname, "w") as f:
            for i in range(len(self.data)):
                f.write(str(self.data[i]))
                f.write('\n')

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.rank_text, self.rank_text_rect)
        self.screen.blit(self.score_text, self.score_text_rect)
        for r in self.table:
            self.screen.blit(r[0], r[1])
            self.screen.blit(r[2], r[3])
