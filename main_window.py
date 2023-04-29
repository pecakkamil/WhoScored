from tkinter import *
import json

# ---------------------------- CONSTANTS ------------------------------- #
FIELD_SIZE = 10
BG_COLOR = "pink"
BORDER_COLOR = "blue"
BORDER_THICKNESS = 2
FRAME_WIDTH = 1000
TEXT_COLOR = "black"
FONT_NAME = "Courier"

# reading league list from file
with open("data/leagues.txt") as file:
    leagues_dict = json.loads(file.read())
    leagues=leagues_dict.keys()


class Window(Tk):
    def __init__(self, get_matches_to_update, matches_already_scraped, scrape_update, scrape_series, create_csv):
        super().__init__()
        self.title("Whoscored.com - database")
        self.config(padx=FIELD_SIZE, pady=FIELD_SIZE, bg=BG_COLOR)

        # frame1 - matches to update -------------------------------------
        f1 = Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=BORDER_THICKNESS,
                        width=FRAME_WIDTH)
        f1.grid(row=0, column=0, sticky="nsew", rowspan=3)
        label = Label(f1, text="Match update", font=(FONT_NAME, 20, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")
        label = Label(f1, text="League selection", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")
        # datatype of menu text
        self.league_menu_match_update_var = StringVar()
        # initial menu text
        self.league_menu_match_update_var.set("England")

        # Create Dropdown menu
        drop = OptionMenu(f1, self.league_menu_match_update_var, *leagues)
        drop.pack()

        self.year_var = StringVar()
        self.month_var = StringVar()
        self.day_var = StringVar()

        year_entry = Entry(f1, textvariable=self.year_var, font=('calibre', 10, 'normal'))
        month_entry = Entry(f1, textvariable=self.month_var, font=('calibre', 10, 'normal'))
        day_entry = Entry(f1, textvariable=self.day_var, font=('calibre', 10, 'normal'))

        label = Label(f1, text="Year:", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")
        year_entry.pack(side="top")

        label = Label(f1, text="Month:", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")
        month_entry.pack(side="top")

        label = Label(f1, text="Day:", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")
        day_entry.pack(side="top")

        self.update_button = Button(f1, text='Search for update', command=get_matches_to_update)
        self.update_button.pack(side="top")

        self.matches_to_update_label = Label(f1, text=f"Matches to update: 0 ", font=(FONT_NAME, 10, "bold"),
                                             fg=TEXT_COLOR, bg=BG_COLOR)
        self.matches_to_update_label.pack(side="top")

        self.matches_frame = Text(f1, height=5, width=30)
        self.matches_frame.pack()

        self.matches_frame.insert(END, "")

        self.check_update_button = Button(f1, text='Check update', command=matches_already_scraped, state=DISABLED)
        self.check_update_button.pack(side="top")

        self.new_matches_label = Label(f1, text=f"New matches: 0 ", font=(FONT_NAME, 10, "bold"),
                                       fg=TEXT_COLOR, bg=BG_COLOR)
        self.new_matches_label.pack(side="top")

        scrape_update_button = Button(f1, text='Scrape update', command=scrape_update)
        scrape_update_button.pack(side="top")

        # frame2 - scrape from series -------------------------------------------------------------
        f2 = Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=BORDER_THICKNESS,
                        width=FRAME_WIDTH)
        f2.grid(row=0, column=1, sticky="nsew")

        label = Label(f2, text="Scraping from series", font=(FONT_NAME, 20, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")

        # datatype of menu text
        self.menu3_var = StringVar()

        # initial menu text
        self.menu3_var.set("England")

        # Create Dropdown menu
        drop = OptionMenu(f2, self.menu3_var, *leagues)
        drop.pack()

        self.start_id = Entry(f2)
        self.end_id = Entry(f2)

        label = Label(f2, text="Start ID", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")
        self.start_id.pack()
        label = Label(f2, text="End ID", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")
        self.end_id.pack()

        scrape_update_button = Button(f2, text='Scrape series', command=scrape_series)
        scrape_update_button.pack(side="top")

        # frame3 - create csv ----------------------------------------------------------------
        f3 = Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=BORDER_THICKNESS,
                        width=FRAME_WIDTH)
        f3.grid(row=1, column=1, sticky="nsew")

        label = Label(f3, text="Creating CSV", font=(FONT_NAME, 20, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")

        label = Label(f3, text="League selection", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")

        # datatype of menu text
        self.menu2_var = StringVar()

        # initial menu text
        self.menu2_var.set("England")

        # Create Dropdown menu
        drop = OptionMenu(f3, self.menu2_var, *leagues)
        drop.pack()

        create_csv_button = Button(f3, text='Create CSV', command=create_csv)
        create_csv_button.pack(side="top")

        # frame4 - cautions  ---------------------------------------------------------------------
        f4 = Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=BORDER_THICKNESS,
                        width=FRAME_WIDTH)
        f4.grid(row=2, column=1, sticky="nsew", columnspan=2)

        label = Label(f4, text="Options", font=(FONT_NAME, 20, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")

        label = Label(f4, text="Sleeping time", font=(FONT_NAME, 10, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")

        spinbox_value = StringVar(value="2")
        spin_box = Spinbox(
            f4,
            from_=0,
            to=5,
            increment=0.1,
            textvariable=spinbox_value,
            wrap=True)
        spin_box.pack(side="top")
        self.sleeping_time = float(spinbox_value.get())

        # frame5 - cautions  ---------------------------------------------------------------------
        f5 = Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=BORDER_THICKNESS,
                        width=FRAME_WIDTH)
        f5.grid(row=3, column=0, sticky="nsew", columnspan=2)

        label = Label(f5, text="Cautions", font=(FONT_NAME, 20, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
        label.pack(side="top")

        self.caution_text = Text(f5, height=5)
        self.caution_text.pack()
        self.caution_text.insert(END, "")
