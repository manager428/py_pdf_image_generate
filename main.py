from reportlab.platypus import SimpleDocTemplate, Image, TableStyle, Table, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import Color, toColor
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from reportlab.pdfbase import pdfmetrics
import util
import requests
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import urllib.request
import shutil
from random import randrange
from PIL import Image
from pathlib import Path
import random
import os

page_width = 8.28
page_height = 11.69
margin_left = 0.15
margin_right = 0.15

def get_news_article(url):
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)
    temp = response.json()
    articles = []
    index = 0
    for item in temp:
        try:
            if item["News_Content"] != '' and item['Title'] != '' and item['Images_Links'] != '':
                if download_image(item['Images_Links'], index, item['Category']):
                    item["Img_down_path"] = "static/images/" + item["Category"] + "/" + str(index) + ".jpg"
                    articles.append(item)
                    index = index +1
        except Exception as e:
            print(e)
    return articles

def is_grey_scale(img_path):
    im = Image.open(img_path)
    width, height = im.size
    if width < 10 or height < 10:
        return True
    return False

def download_image(img_url, index, category):
    # calling urlretrieve function to get resource
    try:
        dir_path = "static/images/" + category
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        filename = dir_path + "/" + str(index)+ ".jpg"
        urllib.request.urlretrieve(img_url, filename)
        if is_grey_scale(filename):
            os.remove(filename)
            return False
    except Exception as e:
        return False
    return True
            
def get_summary_text(article, index):
    long_text = article["News_Content"]
    temp = ''
    try:
        base_url = 'https://private-api.smrzr.io/v1/summarize?num_sentences=10'
        headers = { "api_token": "2e43cfd1-44e9-4e00-b3f7-bc6a04d822c8" }
        resp = requests.post(base_url, headers=headers, data=long_text)
        temp = resp.json()['summary']
    except Exception as e:
        print(e)
        temp = article["News_Content"]
    return temp

def download_image_only(img_url, index):
    # calling urlretrieve function to get resource
    try:
        Path("static/images/top").mkdir(parents=True, exist_ok=True)
        filename = "static/images/top/" + str(index)+ ".jpg"
        urllib.request.urlretrieve(img_url, filename)
        if is_grey_scale(filename):
            return False
    except Exception as e:
        print(e, index)
        return False
    return True

def get_summary_textonly(joined_titles, count_of_sentences):
    temp = joined_titles
    try:
        base_url = 'https://private-api.smrzr.io/v1/summarize?num_sentences=' + str(count_of_sentences)
        headers = { "api_token": "2e43cfd1-44e9-4e00-b3f7-bc6a04d822c8" }
        resp = requests.post(base_url, headers=headers, data=joined_titles)
        temp = resp.json()['summary']
    except Exception as e:
        print(e)
    return temp

def process_nlp_text(summary_text):
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")
    # Process whole documents
    doc = nlp(summary_text)
    store_entity = []
    store_entity_label = []
    for entity in doc.ents:
        store_entity.append(entity.text)
        store_entity_label.append(entity.label_)
        # print(entity.text, entity.label_)
    entity_label_list = [[value1, value2] for [value1, value2] in zip(store_entity_label, store_entity)]
    new_list = [item[1] for item in entity_label_list if ('CARDINAL' or 'ORDINAL') not in item]
    new_list2 = [item.title() for item in new_list] # change the first letter to uppercase
    new_list_set = list(set(new_list2))
    new_string = ' '.join(new_list_set)
    string_len = len(new_string) + 1
    new_string_just = new_string.rjust(string_len)
    return new_string_just

def join_text_same_category(text_list):
    text_unique_category = []
    for text in text_list:
        text_unique_category.append(process_nlp_text(text))
    
    joined_text = ''.join(text_unique_category)
    return joined_text

def plot_word_cloud(joined_txt, category):
    wordcloud = WordCloud(background_color='white', width=2500, height=1600).generate(joined_txt)
    wordcloud.to_file('static/images/' + category + '/wordcloud.png')

def get_top2_article(all_category_articles):
    print("[+] ====== Get top 2 articles of all category articles ====== [+]")
    joined_all_titles = []
    for cate_articles in all_category_articles:
        for article in cate_articles:
            joined_all_titles.append(article["Title"])
    
    joined_all_titles = ". ".join(joined_all_titles)
    top_titles = get_summary_textonly(joined_all_titles, 6)
    arr_top_titles = top_titles.split(". ")
    random.shuffle(arr_top_titles)
    first_article = {}
    second_article = {}
    index = 1
    for cate_articles in all_category_articles:
        for article in cate_articles:
            for tmp in arr_top_titles:
                if article["Title"] == tmp:
                    # get first article
                    if (download_image_only(article["Images_Links"], index)):
                        content = get_summary_textonly(article["News_Content"], 10)
                        if index == 1:
                            first_article = article
                            first_article["News_Content"] = content
                            first_article["Img_down_path"] = "static/images/top/" + str(index)+ ".jpg"
                            index = index + 1
                        elif index == 2:
                            second_article = article
                            second_article["News_Content"] = content
                            second_article["Img_down_path"] = "static/images/top/" + str(index)+ ".jpg"
                            return first_article, second_article
                        # to do list
    return first_article, second_article

def make_first_page(Story, first_article, second_article):
    # ================= First Page ========================
    Story = util.add_header_title(Story)
    Story = util.add_first_page(Story, first_article, second_article)
    Story.append(PageBreak())
    return Story

def make_second_page(Story, t0, art1, art2, art3, art4):
    Story = util.add_wordcloud_page(Story, t0, art1, art2, art3, art4)
    Story.append(PageBreak())
    return Story
    
def make_subquent_page(Story, art1, art2, art3, art4):
    Story = util.add_subquent_page(Story, art1, art2, art3, art4)
    
    Story.append(PageBreak())
    return Story

if __name__ == '__main__':
    categories = [
        {"Category": "corona"}, {"Category": "homepage"},
        {"Category": "uk"},{"Category": "sport"}, 
        {"Category": "lifestyle"}, {"Category": "book"},
        {"Category": "green-living"}, {"Category": "fashion"},
        {"Category": "education"}, {"Category": "boris-johnson"},
        {"Category": "music"}, {"Category": "entertainment"},
        {"Category": "travel"}, {"Category": "politics"}, 
        {"Category": "business"}, {"Category": "technology"},
        {"Category": "world"}, {"Category": "health"}
    ]
    start_date = "2021-08-25"
    end_date = "2021-08-25"
    
    print("[+] ====== Getting news articles ====== [+]")
    all_category_articles = []
    for cate in categories:
        category = cate["Category"]
        url = "http://18.170.225.85/alpha/category/" + category + "/" + start_date + "/" + end_date
        articles = get_news_article(url)
        all_category_articles.append(articles)
    # first_article, second_article = get_top2_article(all_category_articles)
    
    
    pdf_file = "result.pdf"
    
    doc = SimpleDocTemplate(pdf_file, pagesize=((page_width) * inch, (page_height) * inch), title="Photo.pdf", rightMargin=margin_right*inch, leftMargin=margin_left*inch, topMargin=0.15*inch, bottomMargin=0.15*inch)

    print("[+] ====== Generating first page of PDF ====== [+]")
    first_article = {
        "Title": "Covid infection protection waning in double",
        "News_Content": """
        Most people who catch Covid-19 won't become severely ill and get better relatively quickly. But significant numbers have had long-term problems after recovering from the original infection - even if they weren't very ill in the first place.As society reopens, there are fears long Covid could disproportionately affect those not yet fully vaccinated.Guidance for UK health workers describes long Covid as symptoms continuing for more than 12 weeks after an infection - severe or mild - and can't be explained by another cause. According to the NHS, symptoms include:Surveys have identified tens and even hundreds of other complaints. Probably the largest study so far, by University College London (UCL), identified 200 symptoms affecting 10 organ systems in people with long Covid, at higher levels than in people who were fully recovered.  They include hallucinations, insomnia, hearing and vision changes, short-term memory loss and speech and language issues. Others have reported gastro-intestinal and bladder problems, changes to periods and skin conditions.  How severe these symptoms are varies, but many have been left unable to perform tasks like showering, grocery shopping and remembering words.    We don't yet know for sure.One possibility is the infection makes some people's immune systems go into overdrive, attacking not just the virus but their own tissues. That can happen in people who have very strong immune responses.The virus itself getting into and damaging our cells might explain some symptoms like brain fog and a loss of smell and taste, while damage to blood vessels in particular could lead to heart, lung and brain problems. Another theory is that fragments of the virus could remain in the body, possibly lying dormant and then becoming reactivated. This happens with some other viruses, like herpes and the Epstein Barr virus which causes glandular fever. However, there isn't much evidence for this happening with Covid at the moment. It's likely there are several different things going on in different people, to cause such a wide range of problems. This is really difficult to pin down at the moment, because doctors have only just started recording long Covid as an official diagnosis. However, there is a substantial body of research suggesting the condition becomes increasingly likely with age, and is twice as common among women.Some, but not all, long Covid symptoms are more common in people who were very ill or ended up in hospital.  Analysis of several studies and health record databases by King's College London suggested 1-2% of people in their 20s who had the virus would develop long Covid, compared with 5% of people in their 60s. \"But 1-2% of 100,000 cases a day is a lot of people,\" Dr Claire Steves, one of the study's authors, pointed out. And Dr David Strain at the University of Exeter Medical School, who works with patients with long Covid, said most people being referred to his clinic were in their 20s, 30s and 40s. That might be because these symptoms, though slightly less common in younger people, have a bigger impact on them.  This may also change as older people are more likely to be fully vaccinated. Senior author on the UCL paper Dr Athena Akrami said: \"We're going to deal with a big wave of seemingly mild infections where maybe one in seven is going to develop long Covid, and that will be among young people\".   Children are less likely than adults to catch Covid and so by definition less likely to develop long Covid - but some still do. A study from King's College London found that for most, their symptoms were short-lived. But though a proportion of children did have longer-lasting symptoms, 98% had recovered by eight weeks.Remember the official NHS definition involves symptoms that last 12 weeks or more. For those who are struggling with symptoms though, doctors say it is important caregivers to seek advice from their GPs - and that families should be listened to.  There is currently no test - instead it is currently a \"diagnosis of exclusion\", Dr Strain explained, with doctors first ruling out other possible causes.They will make sure tests for other issues like diabetes, thyroid function and iron deficiency are all clear, before giving a diagnosis. According to researchers, a blood test for long Covid could become available in the future. And in research settings more sophisticated tools are already being used to identify organ damage - but you won't be able to get these at a standard GP appointment. Roughly half of people with long Covid reported an improvement in their symptoms after being jabbed - possibly by resetting their immune response or helping the body attack any remaining fragments of the virus, say experts. Vaccination can also help prevent people contracting the virus and developing long Covid in the first place.In England, 89 specialist long Covid assessment centres have been set up.Similar clinics are expected to open in Northern Ireland in the coming months, while in Scotland and Wales patients will be referred to different services by their GPs, depending on their symptoms.At the moment there are no proven drug treatments and the main focus is on managing symptoms and gradually increasing activity. A formal clinical trial into drug treatments is expected to launch soon.
        """,
        "Img_down_path": "static/images/business/1.jpg",
        "Link": "https://www.theguardian.com/global-development/2021/aug/25/oxygen-firms-accused-of-intimidating-mexican-hospitals-during-pandemic"
    }
    second_article = {
        "Title": "Oxygen firms accused of intimidating Mexican hospitals during pandemic",
        "News_Content": """
        The medicines regulator has approved use of the first treatment in the UK using man-made antibodies to prevent and fight coronavirus.Health secretary Sajid Javid said approval of the first drug designed specifically for Covid-19 in the country is fantastic news and he hoped it could be rolled out for patients on the NHS as soon as possible.AdvertisementThe Medicines and Healthcare products Regulatory Agency (MHRA) said the clinical trial data they had assessed has shown Ronapreve may be used to prevent infection, treat symptoms of acute Covid-19 infection and can reduce the likelihood of being admitted to hospital due to the virus.Trials took place before widespread vaccination and before the emergence of virus variants. It is the first monoclonal antibody combination product approved for use in the prevention and treatment of acute infection from the virus for the UK.AdvertisementMonoclonal antibodies are man-made proteins that act like natural human antibodies in the immune system.The drug, developed by pharmaceutical firms Regeneron and Roche, is given either by injection or infusion and acts at the lining of the respiratory system where it binds tightly to the virus and prevents it from gaining access to the cells, the MHRA said.AdvertisementSajid Javid said: The UK is considered a world leader in identifying and rolling out life-saving treatments for Covid-19, once they have been proven safe and effective in our government-backed clinical trials.This is fantastic news from the independent medicines regulator and means the UK has approved its first therapeutic designed specifically for Covid-19.Dominic Lipinski - PA Images via Getty Images Health Secretary Sajid Javid.This treatment will be a significant addition to our armoury to tackle Covid-19  in addition to our world-renowned vaccination programme and life-saving therapeutics dexamethasone and tocilizumab, Javid added.We are now working at pace with the NHS and expert clinicians to ensure this treatment can be rolled out to NHS patients as soon as possible.AdvertisementMHRA interim chief quality and access officer Dr Samantha Atkinson said: We are pleased to announce the approval of another therapeutic treatment that can be used to help save lives and protect against Covid-19.Ronapreve is the first of its kind for the treatment of Covid-19 and, after a meticulous assessment of the data by our expert scientists and clinicians, we are satisfied that this treatment is safe and effective.With no compromises on quality, safety and efficacy, the public can trust that the MHRA have conducted a robust and thorough assessment of all the available data.
        """,
        "Img_down_path": "static/images/business/1.jpg",
        "Link": "https://www.theguardian.com/global-development/2021/aug/25/oxygen-firms-accused-of-intimidating-mexican-hospitals-during-pandemic"
    }
    Story = []
    Story = make_first_page(Story, first_article, second_article)
    
    ######### remove top 2 articles #######
    new_all_cate_arts = []
    for cate_articles in all_category_articles:
        new_cate_arts = []
        for article in cate_articles:
            if article["Title"] != first_article["Title"] and article["Title"] != second_article["Title"] :
                new_cate_arts.append(article)
        new_all_cate_arts.append(new_cate_arts)

    for articles in all_category_articles:
        if len(articles) == 0:
            continue
        print("[+] ====== Generating pdf for Category: " + articles[0]["Category"] + "  ====== [+]")
        
        ### get word cloud ####
        print("[+] ====== Processing summary ====== [+]")
        index = 0
        summary_content_list = []
        for article in articles:
            summary_text = get_summary_text(article, index)
            article["News_Content"] = summary_text
            summary_content_list.append(summary_text)
            index += 1
        
        print("[+] ====== Getting WordCloud iamge ====== [+]")
        joined_text = join_text_same_category(summary_content_list)
        plot_word_cloud(joined_text, articles[0]["Category"])

        print("[+] ====== Generating PDF files ====== [+]")
        title0 = "INSERT YOUR " + articles[0]["Category"] +" TITLE"
        if len(articles) > 5 :
            Story = make_second_page(Story, title0, articles[0], articles[1], articles[2], articles[3])

            # sort article 1, 5, 9 order
            new_arts = sorted(articles[4:len(articles)], key=lambda k: len(k['News_Content']), reverse=True)
            sorted_arts = []
            pages_count = int(len(new_arts)/4)
            if pages_count > 1:
                for i in range(0, pages_count-1):
                    sorted_arts.append(new_arts[i])
                    sorted_arts.append(new_arts[pages_count + i])
                    sorted_arts.append(new_arts[2*pages_count + i])
                    sorted_arts.append(new_arts[3*pages_count + i])

                for i in range(0, pages_count-1):
                    Story = make_subquent_page(Story, sorted_arts[i*4], sorted_arts[i*4 + 1], sorted_arts[i*4 + 2], sorted_arts[i*4 + 3])
    
    doc.build(Story, onFirstPage=util.add_footer, onLaterPages=util.add_header_footer)