# import dropbox
#
# class cloud_storage:
#     def __init__(self, access_token):
#         self.at = access_token
#
#     def uploadFile(self, file_from, file_to):
#         dpx = dropbox.Dropbox(self.at)
#
#         if file_from != '' and file_to != '':
#             dpx.file_upload(file_from, file_to)
#             print("upload successfully")
#         else:
#             print("we need both file loc and storage loc")
#
#     def main(self):
#         print