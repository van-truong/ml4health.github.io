import pandas as pd
import pdb

csv_df = pd.read_csv("poster_assignments.csv")
csv_df['PDFURL'] = ''

camready_df = pd.read_csv("camera_ready.csv")

item_template_str = \
"""
\n
<!-- 12/12 = full width on mobile, 6/12 = 1/2 screen on laptop -->
<div class="col-xs-12 col-md-6"> 
<div class="thumbnail">
    <div class="caption">
        <h5><a href="{{PDFURL}}">{{TITLE}}</a></h5>
        <p>{{AUTHORS}}</p>
    </div>
</div>
</div>
"""

out_md_str = "Title: Papers \nDate: 2017-11-23\n"
out_md_str += (
"""\n
<!-- THIS PAGE SRC IS AUTO GENERATED. At terminal: $ make accepted_posters -->
\n""")

#n_per_row = 100
out_md_str += \
"""
We have accepted 81 short papers for poster presentation at the workshop. This year we have also established a new category and have selected 86 short papers for digital acceptances. 

These are listed below, with links to the paper on arXiv if provided by the authors.

The poster acceptances will appear at two possible poster sessions on Sat. Dec. 8 in Palais des Congres de Montreal.
<ul>
<li><a href="#session1"> Poster Session 1 (11:30-12:30) </a></li>
<li><a href="#session2"> Poster Session 2 (13:20-14:30) </a></li>
</ul>

<a href="#digital">Digital acceptances</a> will be featured on the website and during breaks at the workshop.

<b>Presenters</b>: 
Remember to follow the <a href="poster-and-slide-instructions.html">poster and slide instructions</a>: **Portrait format. Recommended size: 24 inches wide and 32 inches tall.** Digital acceptance slides can be <a href="https://goo.gl/forms/aFd2DKqHSJuDMuoh2">submitted here</a>.

"""

open_div_str = \
"""
<div class="row display-flex" style="display:flex; display:-webkit-flex;  flex-wrap:wrap; margin-top:25px;">
"""
close_div_str = "</div>"

for sessionid, session_title_html in [
        ('AM',
            '<h2><a name="session1">Poster Session 1 (11:30-12:30)</a></h2>'),
        ('PM',
            '<h2><a name="session2">Poster Session 2 (13:30-14:30)</a></h2>'),
        ('DIGITAL',
            '<h2><a name="digital">Digital Acceptances</a></h2>')]:
    out_md_str += session_title_html
    out_md_str += open_div_str
    for item_id, row_obj in enumerate(csv_df.itertuples()):
        row_dict = row_obj.__dict__
        item_str = item_template_str + ""
        if row_dict['SESSION'] != sessionid:
            continue

        q_df = camready_df.query("PAPERID == %d" % row_dict['PAPERID'])
        if q_df.shape[0] == 1:
            # print "CAM READY INFO:"
            # print "===== BEFORE"
            # print row_dict['TITLE']
            # print row_dict['AUTHORS']

            # row_dict['AUTHORS'] = q_df['AUTHORS'].values[0]
            # row_dict['TITLE'] = q_df['TITLE'].values[0]


            url_str = q_df['PDFURL'].values[0]
            if not pd.isnull(url_str) and url_str[:4] == 'http':
                # only keep good arxiv links
                row_dict['PDFURL'] = url_str
            # print "===== AFTER"
            # print row_dict['TITLE']
            # print row_dict['AUTHORS']

        for key, val in row_dict.items():
            default_val = ""
            # if key == 'PDFURL':
            #     default_val = 'javascript:void(0);'
            #     print default_val, '<<<'
            cur_val = str(val)
            if len(cur_val) == 0 or cur_val == 'nan':
                cur_val = default_val
            item_str = item_str.replace("{{%s}}" % str(key), cur_val)
        out_md_str += item_str
    out_md_str += close_div_str

with open("../pages/accepted_posters.md", 'w') as f:
    f.write(out_md_str)