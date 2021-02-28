'''
Set of Web based codes in python
'''

#FS
def DownloadImageFromURL(url, savePath):
    #DS
    # Downloads an image from a web link URL into specified path
    #DE
    #IS
    import requests
    #IE
    f = open(savePath, 'wb')
    f.write(requests.get(url).content)
    f.close()
#FE