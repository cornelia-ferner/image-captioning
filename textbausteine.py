info_title={'english': "CaptioningBoschBot: What does an AI know about art?",
            'german': "CaptioningBoschBot: Was versteht eine KI von Kunst?"}

info_twitter={'english': "Follow @CaptionBoschBot on Twitter to\n"
                         "see more examples of an AI interpreting art.\n"
                         "Like and retweet or leave a comment.",
              'german': "Folge @CaptionBoschBot auf Twitter,\n"
                        "um weitere Beispiele zu sehen.\n"
                        "Like, retweet oder kommentiere die Posts."}

info_title1={'english': "1. Accessing Tweets",
             'german':  "1. Tweets abrufen"}

info_title2={'english': "2. Generating Captions",
             'german': "2. Bildbeschreibung generieren"}

info_title3={'english': "3. Posting Retweets",
             'german': "3. Retweet posten"}

info_paragraph1={'english': "Given Twitter API credentials from a registered Twitter developer account, an API object "
                            "can be instantiated that handles the access to the Twitter stream. Next, Tweets from a "
                            "user can be retrieved by specifying the ID or screen name which is done to access the "
                            "latest Tweets from @BoschBot. The query can be parameterized to exclude replies and "
                            "retweets from the resulting list of Tweets. This result list is parsed for posts "
                            "containing media to extract the corresponding image URL. From this URL, the image is "
                            "loaded and preprocessed.",
                 'german': "Den Zugriff auf den Twitter-Stream regelt ein Twitter-API-Objekt, wofür Zugangsdaten eines "
                           "regristrierten Twitter-Developer-Accounts benötigt werden. Um auf die Tweets des @BoschBot "
                           "zugreifen zu können, muss die ID oder der Screen-Name angegeben werden. Der Anfrage können "
                           "außerdem Parameter hinzugefügt werden, um Antworten oder Retweets aus der zurückgegebenen "
                           "Liste von Tweets zu entfernen. Diese Ergebnisliste wird nach Posts mit inkludierten Medien "
                           "durchsucht, um die zugehörige Bild-URL zu extrahieren. Von dieser URL wird das Bild geladen "
                           "und vorverarbeitet."}

info_paragraph2={'english': "The core of the bot is the image captioning model which is implemented as vision-to-text "
                     "transformer model. This model consists of an encoder that transforms a given image into a latent "
                     "representation and a language model as decoder for transforming the latent representations into a "
                     "textual description. The already pretrained model that was used consists of a Vision Transformer "
                     "(ViT) neural network as encoder and a GPT-2 neural network as decoder. The underlying ViT was "
                     "pretrained on ImageNet. The encoder-decoder model pipeline for image captioning was pretrained "
                     "on the MS COCO captions dataset that consists of over 330,000 images aligned with captions. "
                     "Images from the dataset show real-world scenes with the object(s) of interest mostly centered in "
                     "the picture or prominently in the foreground which is not the case for the Bosch image segments. ",
                 'german': "Das Kernstück des Bots ist das Bildbeschreibungsmodell, das als Vision-to-Text-Transformer "
                           "implementiert ist. Dieses Modell besteht aus einem Koderer, der ein Bild auf eine latente "
                           "Repräsentation abbildet und ein Sprachmodell als Dekodierer, der diese Repräsentation in "
                           "eine textuelle Beschreibung umwandelt. Das verwendete vortrainierte Modell besteht aus "
                           "einem Vision Transformer (ViT) als Kodierer und einem GPT-2 Netzwerk als Dekodierer. Das "
                           "ViT wurde auf ImageNet-Daten vortrainiert. Das gesamte Bildbeschreibungsmodell wurde am MS "
                           "COCO Captions Datensatz traineirt, der aus über 333.000 Bildern mit dazugehörigen "
                           "Beschreibungen besteht. Diese Bilder zeigen realistische Szenen mit zentrierten Objekten "
                           "prominent im Vordergrund, worin diese sich stark von den Bosch-Bildsegmenten unterscheiden."}

info_paragraph3={'english': "The generated caption is passed to the API object to update the status, i.e. post a Tweet. "
                            "In order to retweet the original post, its Tweet ID has to be passed as attachment URL.",
                 'german': "Die erzeugte Bildbeschreibung wird an das API-Objekt übergeben, um den Status zu "
                           "aktualisieren, also um den Tweet zu veröffentlichen. Der Originaltweet wird per Tweet ID "
                           "als Attachment-URL übergeben."}

background_title={'english': "Vision-to-Text Encoding",
                  'german': "Bild-zu-Text-Kodierung"}