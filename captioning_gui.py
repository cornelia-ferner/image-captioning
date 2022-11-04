import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os
import textwrap
import torch
import textbausteine
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer


class MainWindow:
    def __init__(self):
        ## SETTINGS
        # self.window_size = (1700, 800)  # for highres screen
        # self.canvas_size = (1280, 729)  # for highres screen
        # self.baseheight = 150  # for highgres screen
        self.window_size = (1360, 800)
        self.canvas_size = (940, 700)
        self.baseheight = 120

        self.beam_size = 4
        self.seqlen = 16

        self.dragging = False
        self.busy = False
        self.start_point = self.end_point = self.prior_rect = None
        self.cap = ""

        ## THEME
        sg.LOOK_AND_FEEL_TABLE['CaptioningTheme'] = {'BACKGROUND': '#eae8ea',
                                                     'TEXT': '#000000',
                                                     'INPUT': '#b0abc2',
                                                     'TEXT_INPUT': '#000000',
                                                     'SCROLL': '#99CC99',
                                                     'BUTTON': ('#003333', '#b0abc2'),
                                                     'PROGRESS': ('#D1826B', '#CC8019'),
                                                     'BORDER': 1, 'SLIDER_DEPTH': 0,
                                                     'PROGRESS_DEPTH': 0, }
        # Switch to use your newly created theme
        sg.theme('CaptioningTheme')

        ## LOAD IMAGES
        self.fp_easy = os.path.join(os.getcwd(), "Salzburg.png")
        img_easy = Image.open(self.fp_easy, mode='r').resize(self.canvas_size)
        self.img_byte_arr_easy = io.BytesIO()
        img_easy.save(self.img_byte_arr_easy, format='PNG')

        self.fp_hard = os.path.join(os.getcwd(), "earthly_delights_highres_wiki.png")
        img_hard = Image.open(self.fp_hard, mode='r').resize(self.canvas_size)
        self.img_byte_arr_hard = io.BytesIO()
        img_hard.save(self.img_byte_arr_hard, format='PNG')

        # set as default
        if self.fp_easy:
            self.orig_im = Image.open(self.fp_easy).resize(self.canvas_size)
            self.curr_im = self.orig_im.crop((400, 400, 400, 400))

        # LOAD VisionEncoderDecoder
        # loaded locally (otherwise point to: "nlpconnect/vit-gpt2-image-captioning"; extract from hugginface model zoo)
        self.loc = "./vit-gpt2-image-captioning"  # vision encoder-decoder model (from huggingface model zoo)
        self.feature_extractor = ViTFeatureExtractor.from_pretrained(self.loc)
        self.tokenizer = AutoTokenizer.from_pretrained(self.loc)
        self.model = VisionEncoderDecoderModel.from_pretrained(self.loc)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def run(self):
        ## DEFINE LAYOUT
        col = [[sg.Text(textwrap.fill("Wähle mit der Maus einen Bereich im Bild aus und klicke auf \"Beschreibung\".", 22),
                        key="-CAPTION-", size=(65, 4), font="Fira_Sans 24 italic", pad=((0, 0), (10, 0)))],
               [sg.Image(data=self.get_img_data(self.fp_easy, first=True), size=(200, self.baseheight), key="-SNIPPET-")],
               [sg.Button('BESCHREIBUNG', key="GENERATE!", size=(15, 3), font="Fira_Sans 12 bold")],
               [sg.HorizontalSeparator(pad=((0, 0), (25, 25)))],
               [sg.Text("SCHWIERIGKEIT", size=(40, 1), font="Fira_Sans 12 bold")],
               [sg.Radio('einfach', 1, enable_events=True, key='radio_easy', default=True, text_color='black', font="Fira_Sans 12 bold")],
               [sg.Text('Mit Bildern wie diesem wurde die KI trainiert.', key='text_easy', size=(40, 1), font="Fira_Sans 12 italic")],
               [sg.Radio('schwer', 1, enable_events=True, key='radio_hard', text_color='black', font="Fira_Sans 12 bold")],
               [sg.Text("", key='text_hard', size=(40, 3), font="Fira_Sans 12 italic")],
               [sg.HorizontalSeparator(pad=((0, 0), (25, 25)))],
               [sg.Text("(c) 2022, Cornelia Ferner", key="copyright", font="Fira_Sans 10", size=(60, 1),
                        pad=((220, 0), (0, 0)))]]
        tab1 = sg.Tab("Demo",
                      [[sg.Graph(canvas_size=self.canvas_size, graph_bottom_left=(0, 0),
                                 graph_top_right=self.canvas_size, key="-FULL_IMG-",
                                 change_submits=True,  # mouse click events
                                 drag_submits=True), sg.Column(col)]],
                      font="Fira_Sans 14")

        process_info_col = [
            [sg.Text(textbausteine.info_title1['english'], key="title1", size=(80, 1), font="Fira_Sans 16",
                     background_color="white", text_color='black')],
            [sg.Text(textbausteine.info_paragraph1['english'], key="paragraph1", size=(80, 6), font="Fira_Sans 12",
                     background_color='white', text_color='black')],
            [sg.Text(textbausteine.info_title2['english'], key="title2", size=(80, 1), font="Fira_Sans 16",
                     background_color='white', text_color='black')],
            [sg.Text(textbausteine.info_paragraph2['english'],
                     key="paragraph2", size=(80, 9), font="Fira_Sans 12", background_color='white', text_color='black')],
            [sg.Text(textbausteine.info_title3['english'], key="title3", size=(80, 1), font="Fira_Sans 16",
                     background_color='white', text_color='black')],
            [sg.Text(textbausteine.info_paragraph3['english'],
                     key="paragraph3", size=(80, 2), font="Fira_Sans 12", background_color='white', text_color='black')]
        ]
        tab2 = sg.Tab("About",
                      [
                          [sg.Text(textbausteine.info_title['english'], key="info-title", size=(60, 1), font="Fira_Sans 24",
                                   background_color='white', text_color='black', pad=((0, 0), (10, 20)))],
                          [sg.Image(data=self.get_img_data(os.path.join(os.getcwd(), "qr-code_twitter.png"),
                                    maxsize=(100, 100), first=True), size=(100, 100), key='info-qr',
                                    background_color='white'),
                           sg.Text(textbausteine.info_twitter['english'],
                                   key="info-twitter", size=(110, 3), font="Fira_Sans 16", background_color='white', text_color='black'),
                           sg.Radio('English', 1, enable_events=True, key='radio_en', default=True, background_color='white', text_color='black', font="Fira_Sans 12"),
                           sg.Radio('Deutsch', 1, enable_events=True, key='radio_de', background_color='white', text_color='black', font="Fira_Sans 12")],
                          [sg.Image(data=self.get_img_data(os.path.join(os.getcwd(), "twitter_bot.png"),
                                    maxsize=(int(1142*0.8), int(489*0.8)), first=True), size=(int(1142*0.8), int(489*0.8)),
                                    key='info-img', background_color='white', pad=((0, 0), (20, 10))),
                           sg.Column(process_info_col, background_color='white', pad=((5, 0), (20, 0)))],
                      ],
                      background_color="white", font="Fira_Sans 14")


        layout = [[sg.TabGroup([[tab1, tab2]], tab_location="topleft")]]
        self.window = sg.Window("Captioning Bot", layout, size=self.window_size, finalize=True, background_color="#e2dfde",
                                icon="FHSalzburg_Logo.ico")


        # get the elements for ease of use later
        self.graph = self.window["-FULL_IMG-"]
        self.img = self.window["-SNIPPET-"]
        self.caption = self.window["-CAPTION-"]
        # self.graph.draw_image(self.fp, location=(0, 729)) if self.fp else None
        # high-res images needs to be resized: open with PIL, save as byte array and pass to draw_image
        if self.fp_easy:
            self.graph.draw_image(data=self.img_byte_arr_easy.getvalue(), location=(0, self.canvas_size[1]))


        self.event, values = self.window.read()

        try:
            while True:
                # Loading GUI events
                self.event, values = self.window.read()
                if self.event == sg.WIN_CLOSED:
                    break  # exit

                if self.event == "-FULL_IMG-" and not self.busy:  # if there's a "Graph" event, then it's a mouse
                    x, y = values["-FULL_IMG-"]
                    if not self.dragging:
                        self.start_point = (x, y)
                        self.dragging = True
                    else:
                        self.end_point = (x, y)
                    if self.prior_rect:
                        self.graph.delete_figure(self.prior_rect)
                    if None not in (self.start_point, self.end_point):
                        self.prior_rect = self.graph.draw_rectangle(self.start_point, self.end_point, line_color='#b0abc2', line_width=5)   # try red again
                elif self.event.endswith('+UP'):  # The drawing has ended because mouse up
                    # info = window["info"]
                    # info.update(value=f"grabbed rectangle from {start_point} to {end_point}")
                    if self.start_point and self.end_point:
                        self.img.set_size((None, self.baseheight))
                        start_x = start_y = end_x = end_y = 0
                        ## Fallunterscheidung:
                        if self.start_point[0] < self.end_point[0]:  # start ist links von end
                            start_x = self.start_point[0]
                            end_x = self.end_point[0]
                        else:  # start liegt rechts von end -> tauschen
                            start_x = self.end_point[0]
                            end_x = self.start_point[0]
                        if self.start_point[1] < self.end_point[1]:  # start liegt unter end -> tauschen
                            start_y = self.end_point[1]
                            end_y = self.start_point[1]
                        else:  # start liegt über end
                            start_y = self.start_point[1]
                            end_y = self.end_point[1]
                        self.start_point = (start_x, start_y)
                        self.end_point = (end_x, end_y)
                        self.curr_im = self.orig_im.crop((self.start_point[0], self.canvas_size[1] - self.start_point[1], self.end_point[0], self.canvas_size[1] - self.end_point[1]))
                        if float(self.curr_im.size[1]) > 0:
                            hpercent = (self.baseheight / float(self.curr_im.size[1]))
                            wsize = int((float(self.curr_im.size[0]) * float(hpercent)))
                            self.curr_im = self.curr_im.resize((wsize, self.baseheight))
                        self.img.update(data=ImageTk.PhotoImage(self.curr_im))
                    self.caption.update(value="")
                    self.start_point, self.end_point = None, None  # enable grabbing a new rect
                    self.dragging = False
                elif self.event == 'GENERATE!':  # button
                    self.window['GENERATE!'].update(text="...", disabled=True)
                    self.busy = True
                    self.generate_caption()
                elif self.event == 'Finished':  # triggered, when generate_caption() finishes
                    self.busy = False
                    self.cap = textwrap.fill(values['Finished'], 22)
                    self.caption.update(value=self.cap, font="Fira_Sans 24")
                    self.window['GENERATE!'].update(text="Beschreibung", disabled=False)
                elif self.event == 'radio_easy':  # easy = true  --> Salzburg
                    self.graph.draw_image(data=self.img_byte_arr_easy.getvalue(), location=(0, self.canvas_size[1]))
                    self.window['text_easy'].update(value="Mit Bildern wie diesem wurde die KI trainiert.")
                    self.window['text_hard'].update(value="")
                    self.orig_im = Image.open(self.fp_easy).resize(self.canvas_size)
                    self.curr_im = self.orig_im.crop((400, 400, 400, 400))
                    self.caption.update(
                        textwrap.fill("Wähle mit der Maus einen Bereich im Bild aus und klicke auf \"Beschreibung\".",
                                      22), font="Fira_Sans 24 italic")
                elif self.event == 'radio_hard':  # hard = true  --> Bosch
                    self.graph.draw_image(data=self.img_byte_arr_hard.getvalue(), location=(0, self.canvas_size[1]))
                    self.window['text_easy'].update(value="")
                    self.window['text_hard'].update(
                        value=textwrap.fill(
                            "Bilder wie dieses (ein Kunstwerk von Hieronymus Bosch) hat die KI noch nie gesehen."))
                    self.orig_im = Image.open(self.fp_hard).resize(self.canvas_size)
                    self.curr_im = self.orig_im.crop((400, 400, 400, 400))
                    self.caption.update(
                        textwrap.fill("Wähle mit der Maus einen Bereich im Bild aus und klicke auf \"Beschreibung\".",
                                      22), font="Fira_Sans 24 italic")
                else:
                    print("unhandled event", self.event, values)
        finally:
            self.window.close()

    def generate_step(self):
        pixel_values = self.feature_extractor(images=self.curr_im.convert("RGB"), return_tensors="pt").pixel_values.to(self.device)
        output_ids = self.model.generate(pixel_values, max_length=self.seqlen, num_beams=self.beam_size)
        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]

        return preds

    def get_img_data(self, f, maxsize=(400, 400), first=False):
        """Generate image data using PIL
        """
        img = Image.open(f)
        img.thumbnail(maxsize)
        if first:  # tkinter is inactive the first time
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
        return ImageTk.PhotoImage(img)

    def generate_caption(self):
        pred_caption = self.generate_step()[0]
        pred_caption = pred_caption[0].upper() + pred_caption[1:] + "."
        self.window.write_event_value('Finished', pred_caption)


if __name__ == '__main__':
    MainWindow().run()


