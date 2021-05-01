from google_images_download import google_images_download


class TextToImage:
    def __init__(self, n_images=1):
        self.n_images = n_images
        self.response = google_images_download.googleimagesdownload()

    def __call__(self, text):
        assert isinstance(text, str)
        self.downloadimages(text)

    def downloadimages(self, query):
        arguments = {"keywords": query,
                     "format": "jpg",
                     "limit": self.n_images,
                     "print_urls": False,
                     "size": "medium",
                     "aspect_ratio": "square"}
        try:
            self.response.download(arguments)

        except FileNotFoundError:
            arguments = {"keywords": query,
                         "format": "jpg",
                         "limit": 4,
                         "print_urls": False,
                         "size": "medium"}

            try:
                self.response.download(arguments)
            except:
                pass
