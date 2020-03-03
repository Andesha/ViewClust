from datetime import datetime
import glob

def summary_page(folder_list, page_name):
    """Builds an html page containing links to all html files in a list of folders.

    There's probably a library to do this properly but I just wanted something low level for now.

    Parameters
    -------
    folder_list:Generates the input frames for this function.
        List of folders to check for html files.
    page_name: str
        Output html page name

    See Also
    -------
    useSuite: Generates multiple figures per account
    """

    out_page = """
    <!DOCTYPE html>
    <html>
    <body>

    <h1>ViewClust Summary Page: """ + str(datetime.now())+  """</h1> """

    for folder in folder_list:
        out_page += '<h2>' + folder + '</h2>'
        for plot in glob.glob(folder+'/*.html'):
            out_page += '<a href="'+plot+'">'+plot+'</a><br>'

    out_page += """
    </body>
    </html>
    """

    # Dump string as html page
    with open(page_name, 'w') as f_out:
        f_out.write(out_page)
