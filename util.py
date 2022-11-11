from reportlab.platypus import SimpleDocTemplate, Image, TableStyle, Table, Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import Color, toColor
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics


pdfmetrics.registerFont(TTFont('ARIALI', 'static/fonts/ARIALNI.TTF'))
pdfmetrics.registerFont(TTFont('ARIALN', 'static/fonts/ARIALN.TTF'))
pdfmetrics.registerFont(TTFont('ARIALNB', 'static/fonts/ARIALNB.TTF'))
pdfmetrics.registerFont(TTFont('ARIALB', 'static/fonts/ariblk.ttf'))
pdfmetrics.registerFont(TTFont('FRADMCN', 'static/fonts/FRADMCN.ttf'))
pdfmetrics.registerFont(TTFont('EnglishTowne', 'static/fonts/EnglishTowne.ttf'))

registerFontFamily('ARIALI', normal='ARIALI', bold='ARIALI', italic='ARIALI', boldItalic='ARIALI')
registerFontFamily('ARIALB', normal='ARIALB', bold='ARIALB', italic='ARIALB', boldItalic='ARIALB')
registerFontFamily('ARIALN', normal='ARIALN', bold='ARIALN', italic='ARIALN', boldItalic='ARIALN')
registerFontFamily('ARIALNB', normal='ARIALNB', bold='ARIALNB', italic='ARIALNB', boldItalic='ARIALNB')
registerFontFamily('FRADMCN', normal='FRADMCN', bold='FRADMCN', italic='FRADMCN', boldItalic='FRADMCN')
registerFontFamily('EnglishTowne', normal='EnglishTowne', bold='EnglishTowne', italic='EnglishTowne', boldItalic='EnglishTowne')

page_width = 8.28
page_height = 11.69
margin_left = 0.15
margin_right = 0.15
cell_w = (page_width - margin_right - margin_left) * inch - 12
extra_text_link = "For more information referrer to the source of the article"
def add_header_title(Story):
    
    tblstyle = TableStyle([
        ('BACKGROUND', (0, 0), (0, 1), toColor('rgb(255, 195, 0)')),
        ('ALIGN', (0, 0), (0, 1), 'CENTER'),
        ('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
        ('VALIGN', (0, 1), (0, 1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0),
        ('TOPPADDING', (0, 1), (0, 1), 0),
    ])

    style_background = ParagraphStyle(
        name="content",
        fontSize=34,
        fontName='ARIALI',
        textColor=colors.black,
    )
    style_title = ParagraphStyle(
        name="title",
        fontSize=92,
        textColor=colors.black,
        fontName='FRADMCN',
        alignment=1,
    )

    cell1 = Paragraph('THE', style_background)
    cell2 = Paragraph('TRENDI WEEK', style_title)

    tbl = Table([[cell1], [cell2]], colWidths=[cell_w], rowHeights=[20, 110])
    tbl.setStyle(tblstyle)
    Story.append(tbl)

    Story.append(Spacer(1, 8))
    tblstyle = TableStyle([
        ('FONT', (0, 0), (1, 0), 'ARIALI', 12),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, toColor("rgb(0, 0, 0)")),
        ('LINEABOVE', (0, 0), (-1, 0), 1.5, toColor("rgb(0, 0, 0)")),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 1), (0, 1), 5),
        ('BOTTOMPADDING', (0, 0), (1, 0), 5),
    ])
    tbl = Table([['ALL ABOUT THE BIG WORLD WE LIVE IN', 'EXCLUSIVE WEEKLY NEWS']],
                colWidths=[cell_w / 2, cell_w / 2])
    tbl.setStyle(tblstyle)
    Story.append(tbl)
    Story.append(Spacer(1, 10))
    return Story

def add_first_page(Story, cart1, cart2):
    art1 = cart1
    art2 = cart2
    # top first article
    style_head = ParagraphStyle(
        name="title",
        backColor=toColor("rgb(128, 128, 128)"),
        textColor=toColor("rgb(255, 255, 255)"),
        fontName="ARIALB",
        fontSize=24,
        alignment=TA_LEFT,
        leading=25,
        borderPadding=(0, 0, 5),
    )
    tit_art1 = art1["Title"]
    tit_art2 = art2["Title"]
    cnt_art1 = art1["News_Content"]
    cnt_art2 = art2["News_Content"]
    Story.append(Paragraph(tit_art1, style_head))
    Story.append(Spacer(1, 12))
    tblstyle = TableStyle([
        ('FONT', (0, 0), (1, 0), 'ARIALI', 11),
        ('ALIGN', (0, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (1, 0), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    style_content = ParagraphStyle(
        name="title",
        fontSize=10,
        alignment= TA_JUSTIFY,
        borderpadding =0,
    )
    first_image = Image(art1["Img_down_path"])
    first_image.drawWidth = cell_w * 2/3 - 6
    first_image.drawHeight = (cell_w * 2/3 - 6) * 9/ 16
    limit_count1 = 1460
    if len(tit_art2) >= 100 and len(tit_art1) >= 70:
        if len(tit_art1) > 80 :
            limit_count1 = 1300
        else:
            limit_count1 = 1200
    elif len(tit_art2) >= 100 or len(tit_art1) >= 65:
        if len(tit_art1) > 80 :
            limit_count1 = 1300
        else:
            limit_count1 = 1400

    if len(cnt_art1) > limit_count1:
        cnt_art1 = cnt_art1[0: limit_count1]
    
    cnt_art1 = get_sentence(cnt_art1, limit_count1, art1["Link"])

    length_cnt_art1 = len(cnt_art1)
    if art1["Link"] in cnt_art1:
        length_cnt_art1 = len(cnt_art1) - len(art1['Link']) - 34
    
    cnt_art1_1 = cnt_art1[0: int(length_cnt_art1*11/30)]
    cnt_art1_2 = cnt_art1[int(length_cnt_art1*11/30): len(cnt_art1) ]
    
    cell1 = [first_image, Spacer(1, 7), Paragraph(cnt_art1_1, style_content)]
    cell2 = [Paragraph(cnt_art1_2, style_content)]
    tbl = Table([[
        cell1,
        cell2
    ]], colWidths=[cell_w * 2/3, cell_w * 1/3])
    tbl.setStyle(tblstyle)
    Story.append(tbl)
    Story.append(Spacer(1, 4))
    
    # top second article
    style_title = ParagraphStyle(
        name="title1",
        textColor=toColor("rgb(0, 0, 0)"),
        fontName="ARIALB",
        fontSize=18,
        leading=18,
        alignment=TA_LEFT,
    )
    Story.append(Paragraph(tit_art2, style_title))
    Story.append(Spacer(1, 6))
    tblstyle = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'ARIALI', 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), 6),
        ('LEFTPADDING', (1, 0), (1, 0), 3),
        ('RIGHTPADDING', (1, 0), (1, 0), 3),
        ('RIGHTPADDING', (2, 0), (2, 0), 0),
        ('LEFTPADDING', (2, 0), (2, 0), 6),
    ])

    second_img = Image(art2["Img_down_path"])
    second_img.drawWidth = cell_w * 1/3 - 6
    second_img.drawHeight = (cell_w * 1/3 - 6) * 9/ 16
    
    
    limit_count2 = 1490
    if len(cnt_art2) > limit_count2:
        cnt_art2 = cnt_art2[0: limit_count2]
    
    cnt_art2 = get_sentence(cnt_art2, limit_count2, art2["Link"])

    length_cnt_art2 = len(cnt_art2)
    print(length_cnt_art2)
    if art2["Link"] in cnt_art2:
        length_cnt_art2 = len(cnt_art2) - len(art2['Link']) - 34
    
    len_cnt_art2 = length_cnt_art2 - int(length_cnt_art2/6)
    print(len_cnt_art2/2, len_cnt_art2)

    cnt_art2_1 = cnt_art2[0: int(len_cnt_art2 / 2)]
    cnt_art2_2 = cnt_art2[int(len_cnt_art2 / 2): len_cnt_art2 ]
    cnt_art2_3 = cnt_art2[len_cnt_art2: len(cnt_art2) ]

    cell3 = [second_img, Spacer(1, 7), Paragraph(cnt_art2_3, style_content)]
    tbl = Table([[Paragraph(cnt_art2_1, style_content), Paragraph(cnt_art2_2, style_content), cell3]],
                colWidths=[cell_w /3, cell_w /3, cell_w /3])
    tbl.setStyle(tblstyle)
    Story.append(tbl)
    return Story

def add_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    # Footer
    hr_line = HRFlowable(
        width="100%",
        thickness=1, 
        lineCap='round', 
        color=toColor("rgb(0, 0, 0)"), 
        spaceBefore=1, 
        spaceAfter=1, 
        hAlign='CENTER', 
        vAlign='BOTTOM', 
        dash=None
    )
    tblstyle = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'ARIALI', 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (0, 0), 6),
        ('TOPPADDING', (2, 0), (2, 0), 6),
        ('TOPPADDING', (1, 0), (1, 0), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ])

    style_background = ParagraphStyle(
        name="title",
        fontSize=10,
        alignment= TA_CENTER,
    )
    text = "<b>trendiworldnews.com</b>"
    text_width = 120

    tbl = Table([[hr_line, Paragraph(text, style_background), hr_line]],
                colWidths=[(cell_w - text_width)*1/2, text_width, (cell_w -text_width)*1/2])
    tbl.setStyle(tblstyle)
    w, h = tbl.wrap(doc.width, doc.bottomMargin)
    tbl.drawOn(canvas, doc.leftMargin, h)

    # Release the canvas
    canvas.restoreState()

def add_header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    # header
    tblstyle1 = TableStyle([
        ('FONT', (0, 0), (1, 0), 'ARIALI', 12),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, toColor("rgb(0, 0, 0)")),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 1), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ])
    tbl1 = Table([['ALL ABOUT THE BIG WORLD WE LIVE IN', 'EXCLUSIVE WEEKLY NEWS']],
                colWidths=[cell_w / 2, cell_w / 2])
    tbl1.setStyle(tblstyle1)
    
    w, h = tbl1.wrap(doc.width, doc.topMargin)
    tbl1.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
    
    # Footer
    hr_line = HRFlowable(
        width="100%",
        thickness=1, 
        lineCap='round', 
        color=toColor("rgb(0, 0, 0)"), 
        spaceBefore=1, 
        spaceAfter=1, 
        hAlign='CENTER', 
        vAlign='BOTTOM', 
        dash=None
    )
    tblstyle = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'ARIALI', 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (0, 0), 6),
        ('TOPPADDING', (2, 0), (2, 0), 6),
        ('TOPPADDING', (1, 0), (1, 0), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ])

    style_background = ParagraphStyle(
        name="title",
        fontSize=10,
        alignment= TA_CENTER,
    )
    text = "<b>trendiworldnews.com</b>"
    text_width = 120

    tbl = Table([[hr_line, Paragraph(text, style_background), hr_line]],
                colWidths=[(cell_w - text_width)*1/2, text_width, (cell_w -text_width)*1/2])
    tbl.setStyle(tblstyle)
    w, h = tbl.wrap(doc.width, doc.bottomMargin)
    tbl.drawOn(canvas, doc.leftMargin, h)

    # Release the canvas
    canvas.restoreState()
         
def get_sentence(text, limit, link):
    x_dot = text.rfind(".")
    x_comma = text.rfind(",")
    x_question_mark = text.rfind("?")
    res_text = ""
    if x_dot == -1 and x_comma == -1 and x_question_mark == -1:
        res_text = text
    if x_dot > x_comma and x_dot > x_question_mark:
        res_text = text[0: x_dot + 1]
    if x_comma > x_dot and x_comma > x_question_mark:
        res_text = text[0: x_comma + 1]
    if x_question_mark > x_dot and x_question_mark > x_comma:
        res_text = text[0: x_comma + 1]

    if (limit - len(res_text)) > len(extra_text_link) - 5:
        res_text = res_text + "   <b><a href='"+link+"'>" + extra_text_link + "</a></b>"
    res_text = res_text.replace("�", "£")
    return res_text

def add_subquent_page(Story, cart1, cart2, cart3, cart4):
    old_arts = [cart1, cart2, cart3, cart4]
    new_arts = sorted(old_arts, key=lambda k: len(k['News_Content']), reverse=True)
    art1 = new_arts[0]
    art2 = new_arts[3]
    art3 = new_arts[1]
    art4 = new_arts[2]
    Story.append(Spacer(1, 20))
    style_text = ParagraphStyle(
        name="text",
        fontSize=10,
        alignment= TA_JUSTIFY,
        borderpadding =0,
        
    )
    style_subtitle = ParagraphStyle(
        name="subtitle",
        textColor=toColor("rgb(0, 0, 0)"),
        fontName="ARIALB",
        fontSize= 12,
        leading=12,
        alignment=TA_LEFT,
        
    )
    style_title = ParagraphStyle(
        name="title",
        textColor=toColor("rgb(0, 0, 0)"),
        fontName="ARIALB",
        fontSize= 16,
        alignment=TA_LEFT,
        leading=17,
        borderPadding=(0, 0, 10),
        
    )
    
    tblstyle_col_3 = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'ARIALI', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    img_art1 = Image(art1["Img_down_path"])
    img_art1.drawWidth = cell_w * 3/4 - 6
    img_art1.drawHeight = (cell_w * 3/4 - 6) / 2
    cnt_art1 = art1["News_Content"]
    tit_art1 = art1["Title"]
    tit_art2 = art2["Title"]
    limit_count1 = 1630
    if len(tit_art2) >= 85 and len(tit_art1) >= 85:
        limit_count1 = 1540
    elif len(tit_art2) >= 85 or len(tit_art1) >= 85:
        limit_count1 = 1560

    if len(cnt_art1) > limit_count1:
        cnt_art1 = cnt_art1[0: limit_count1]
    
    cnt_art1 = get_sentence(cnt_art1, limit_count1, art1["Link"])
    length_cnt_art1 = len(cnt_art1)
    if art1["Link"] in cnt_art1:
        length_cnt_art1 = len(cnt_art1) - len(art1['Link']) - 34
    
    cnt_art1_1 = cnt_art1[0: int(length_cnt_art1/3)]
    cnt_art1_2 = cnt_art1[int(length_cnt_art1/3): int(length_cnt_art1*2/3) ]
    cnt_art1_3 = cnt_art1[int(length_cnt_art1*2/3): len(cnt_art1) ]

    ######## first article ####
    tbl_3_cols = Table([[
        Paragraph(cnt_art1_1, style_text),
        Paragraph(cnt_art1_2, style_text),
        Paragraph(cnt_art1_3, style_text),
    ]], colWidths=[cell_w * 1/4, cell_w * 1/4, cell_w * 1/4])
    tbl_3_cols.setStyle(tblstyle_col_3)
    
    ####### second article #####
    img_art2 = Image(art2["Img_down_path"])
    img_art2.drawWidth = cell_w / 2 - 12
    img_art2.drawHeight = 2.4 * inch
    cnt_art2 = art2["News_Content"]
    
    if len(cnt_art2) > 430:
        cnt_art2 = cnt_art2[0: 430]
    
    cnt_art2 = get_sentence(cnt_art2, 430, art2["Link"])

    tbl_2_cols = Table([[
        Paragraph(cnt_art2, style_text),
        img_art2
    ]], colWidths=[cell_w * 1/4, cell_w * 2/4])
    tbl_2_cols.setStyle(tblstyle_col_3)
    
    ####### add first and second article to pdf ######
    cell1 = [
        Paragraph(tit_art1, style_title), Spacer(1, 6), img_art1, Spacer(1, 4), tbl_3_cols, Spacer(1, 5), 
        Paragraph(tit_art2, style_title), Spacer(1, 4), tbl_2_cols
    ]

    ####### third article #########
    img_art3 = Image(art3["Img_down_path"])
    img_art3.drawWidth = cell_w * 1/4 - 6
    img_art3.drawHeight = (cell_w * 1/4 - 6)/2
    cnt_art3 = art3["News_Content"]
    tit_art3 = art3["Title"]
    limit_count3 = 550
    if len(tit_art3) > 100:
        limit_count3 = 460
    elif len(tit_art3) > 75:
        limit_count3 = 480
    elif len(tit_art3) > 62:
        limit_count3 = 520

    if len(cnt_art3) > limit_count3:
        cnt_art3 = cnt_art3[0: limit_count3]
    
    cnt_art3 = get_sentence(cnt_art3, limit_count3, art3["Link"])

    ####### fourth article #########
    img_art4 = Image(art4["Img_down_path"])
    img_art4.drawWidth = cell_w * 1/4 - 6
    img_art4.drawHeight = (cell_w * 1/4 - 6)/2
    cnt_art4 = art4["News_Content"]
    tit_art4 = art4["Title"]
    limit_count4 = 550
    if len(tit_art4) > 100:
        limit_count4 = 460
    elif len(tit_art3) > 75:
        limit_count4 = 480
    elif len(tit_art4) > 62:
        limit_count4 = 520
    if len(cnt_art4) > limit_count4:
        cnt_art4 = cnt_art4[0: limit_count4]
    
    cnt_art4 = get_sentence(cnt_art4, limit_count4, art4["Link"])
    cell2 = [
        Paragraph(tit_art3, style_subtitle), Spacer(1, 2), Paragraph(cnt_art3, style_text), Spacer(1, 3), img_art3, Spacer(1, 4), 
        Paragraph(tit_art4, style_subtitle), Spacer(1, 2), Paragraph(cnt_art4, style_text), Spacer(1, 3), img_art4
    ]
    
    tblstyle_content = TableStyle([
        ('BACKGROUND', (1, 0), (1, 0), toColor("rgb(230, 230, 230)")),
        ('FONT', (0, 0), (-1, -1), 'ARIALI', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('TOPPADDING', (0, 1), (0, 1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ])
    tbl = Table([[
        cell1,
        cell2
    ]], colWidths=[cell_w * 3/4, cell_w * 1/4])
    tbl.setStyle(tblstyle_content)
    Story.append(tbl)
    return Story

def add_wordcloud_page(Story, title0, cart1, cart2, cart3, cart4):
    old_arts = [cart1, cart2, cart3, cart4]
    new_arts = sorted(old_arts, key=lambda k: len(k['News_Content']), reverse=True)
    art1 = new_arts[0]
    art2 = new_arts[3]
    art3 = new_arts[1]
    art4 = new_arts[2]

    img_award_path = "static/images/" + cart1["Category"] + "/wordcloud.png"
    Story.append(Spacer(1, 20))
    
    style_text = ParagraphStyle(
        name="text",
        fontSize=10,
        alignment= TA_JUSTIFY,
        borderpadding =0,
        
    )
    style_subtitle = ParagraphStyle(
        name="subtitle",
        textColor=toColor("rgb(0, 0, 0)"),
        fontName="ARIALB",
        fontSize= 12,
        alignment=TA_LEFT,
        
    )
    style_head = ParagraphStyle(
        name="head",
        textColor=toColor("rgb(0, 0, 0)"),
        fontName="ARIALB",
        fontSize= 21,
        alignment=TA_LEFT,
        leading=21,
        
    )
    style_title = ParagraphStyle(
        name="title",
        textColor=toColor("rgb(0, 0, 0)"),
        fontName="ARIALB",
        fontSize= 16,
        alignment=TA_LEFT,
        leading=17,
        
    )
    img_head = Image(img_award_path)
    img_head.drawWidth = cell_w * 3/4 - 6
    img_head.drawHeight = 3.6 * inch
    

    tblstyle_col_3 = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'ARIALI', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    img_art1 = Image(art1["Img_down_path"])
    img_art1.drawWidth = cell_w * 1/4 - 12
    img_art1.drawHeight = 2.6 * inch
    cnt_art1 = art1["News_Content"]
    tit_art1 = art1["Title"]
    tit_art2 = art2["Title"]

    limit_count1 = 900
    if len(tit_art2) >= 88 and len(tit_art1) >= 88:
        limit_count1 = 780
    elif len(tit_art2) >= 88 or len(tit_art1) >= 88:
        limit_count1 = 850

    if len(cnt_art1) > limit_count1:
        cnt_art1 = cnt_art1[0: limit_count1]
    
    cnt_art1 = get_sentence(cnt_art1, limit_count1, art1["Link"])

    length_cnt_art1 = len(cnt_art1)
    if art1["Link"] in cnt_art1:
        length_cnt_art1 = len(cnt_art1) - len(art1['Link'])

    cnt_art1_1 = cnt_art1[0: int(length_cnt_art1/2)]
    cnt_art1_2 = cnt_art1[int(length_cnt_art1/2): len(cnt_art1) ]

    ######## first article ####
    tbl_3_cols = Table([[
        Paragraph(cnt_art1_1, style_text),
        Paragraph(cnt_art1_2, style_text),
        img_art1
    ]], colWidths=[cell_w * 1/4, cell_w * 1/4, cell_w * 1/4])
    tbl_3_cols.setStyle(tblstyle_col_3)
    
    ####### second article #####
    img_art2 = Image(art2["Img_down_path"])
    img_art2.drawWidth = cell_w / 2 - 12
    img_art2.drawHeight = 2.4 * inch
    cnt_art2 = art2["News_Content"]
    
    if len(cnt_art2) > 400:
        cnt_art2 = cnt_art2[0: 400]
        cnt_art2 = get_sentence(cnt_art2, 400, art2["Link"])
    tbl_2_cols = Table([[
        Paragraph(cnt_art2, style_text),
        img_art2
    ]], colWidths=[cell_w * 1/4, cell_w * 2/4])
    tbl_2_cols.setStyle(tblstyle_col_3)
    
    ####### add first and second article to pdf ######
    cell1 = [
        Paragraph(title0, style_head), Spacer(1, 6), img_head, Spacer(1, 5), 
        Paragraph(tit_art1, style_title), tbl_3_cols, Spacer(1, 5), 
        Paragraph(tit_art2, style_title), Spacer(1, 5), tbl_2_cols
    ]

    ####### third article #########
    img_art3 = Image(art3["Img_down_path"])
    img_art3.drawWidth = cell_w * 1/4 - 6
    img_art3.drawHeight = (cell_w * 1/4 - 6)/2
    cnt_art3 = art3["News_Content"]
    tit_art3 = art3["Title"]
    limit_count3 = 550
    if len(tit_art3) > 100:
        limit_count3 = 460
    elif len(tit_art3) > 75:
        limit_count3 = 480
    elif len(tit_art3) > 62:
        limit_count3 = 520
    if len(cnt_art3) > limit_count3:
        cnt_art3 = cnt_art3[0: limit_count3]
    
    cnt_art3 = get_sentence(cnt_art3, limit_count3, art3["Link"])

    ####### fourth article #########
    img_art4 = Image(art4["Img_down_path"])
    img_art4.drawWidth = cell_w * 1/4 - 6
    img_art4.drawHeight = (cell_w * 1/4 - 6)/2
    cnt_art4 = art4["News_Content"]
    tit_art4 = art4["Title"]
    limit_count4 = 550
    if len(tit_art4) > 100:
        limit_count4 = 460
    elif len(tit_art4) > 75:
        limit_count4 = 480
    elif len(tit_art4) > 62:
        limit_count4 = 520
    if len(cnt_art4) > limit_count4:
        cnt_art4 = cnt_art4[0: limit_count4]
    
    cnt_art4 = get_sentence(cnt_art4, limit_count4, art4["Link"])
    cell2 = [
        Paragraph(tit_art3, style_subtitle), Spacer(1, 5), Paragraph(cnt_art3, style_text), Spacer(1, 5), img_art3, Spacer(1, 7), 
        Paragraph(tit_art4, style_subtitle), Spacer(1, 5), Paragraph(cnt_art4, style_text), Spacer(1, 5), img_art4, Spacer(1, 7)
    ]
    
    tblstyle_content = TableStyle([
        ('BACKGROUND', (1, 0), (1, 0), toColor("rgb(230, 230, 230)")),
        ('FONT', (0, 0), (-1, -1), 'ARIALI', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 1), (0, 1), 10),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ])
    tbl = Table([[
        cell1,
        cell2
    ]], colWidths=[cell_w * 3/4, cell_w * 1/4])
    tbl.setStyle(tblstyle_content)
    Story.append(tbl)
    return Story
