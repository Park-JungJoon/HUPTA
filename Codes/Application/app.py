import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List
from collections import defaultdict
from shiny import *
from shiny.types import NavSetArg
from shiny.ui import div, em
from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from shiny.types import NavSetArg
from htmltools import HTML, div
import asyncio
from datetime import date
import numpy as np
from download_functions import *

media = os.getcwd() + '/media/'

genes = ["Example"]
genes = genes + list(gene_setting()[0])
symboldict = {}
with open (media + 'gene_match.tsv') as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        gene = line.split('\t')[0]
        if gene not in genes:
            continue
        symbol = line.split('\t')[1]
        symboldict[gene] = symbol


table_style = "border-right: 1px solid #ccc; padding-right: 10px; text-align: center; border-collapse: separate; border-spacing: 2px; border-left: 1px solid #ccc;"
gene_input = defaultdict(str)
for gene in genes:
    if gene != 'Example':
        gene_input[gene] = gene + ' (' +symboldict[gene] +')'
    if gene == 'Example':
        gene_input[gene] = gene
    

tissue_selectize = {'Adipose Tissue' : 'Adipose Tissue','Adrenal Gland' : 'Adrenal Gland','Bladder' : 'Bladder','Blood' : 'Blood',
                    'Blood Vessel' : 'Blood Vessel','Brain' : 'Brain','Breast' : 'Breast','Esophagus' : 'Esophagus','Heart' : 'Heart',
                    'Kidney' : 'Kidney','Large Intestine' : 'Large Intestine','Liver' : 'Liver','Lung' : 'Lung',
                    'Lymph Nodes' : 'Lymph Nodes','Muscle' : 'Muscle','Ovary' : 'Ovary','Pancreas' : 'Pancreas','Pituitary' : 'Pituitary',
                    'Prostate' : 'Prostate','Skin' : 'Skin','Small Intestine' : 'Small Intestine','Spleen' : 'Spleen',
                    'Stomach' : 'Stomach','Testis' : 'Testis','Thymus' : 'Thymus','Thyroid' : 'Thyroid',
                    'Tibial Nerve' : 'Tibial Nerve','Uterus' : 'Uterus','Vagina' : 'Vagina'}

with open('help_page_center.html', 'r') as file:
    help_page = file.read()

with open ('about_page.html','r') as file:
    about_page = file.read()

app_ui = ui.page_navbar(
        ui.nav("About",
            ui.HTML(about_page),
           ),
    ui.nav("Data",
        ui.row(
            ui.column(
                3,
                ui.panel_well(
                    ui.input_selectize(
                        "search_box",
                        "Select Gene To See",
                        gene_input,
                    ),),
                ui.div({"class": "card"},ui.output_ui("gene_link"),), # gene hyperlink
                ui.div(
                    {"class": "card"},
                    ui.input_action_button("popup_geneset", "Gene Set Description"),
                    ui.input_action_button("popup_parameter", "Parameter Description"),
                    ui.input_action_button("popup_img_ts_score_distribution", "TS Score Distribution"),
                    ui.input_action_button("popup_img_constitive_score_distribution", "Consecutive Score Distribution"),
                    ui.input_action_button("popup_img_cv_distribution", "CV Distribution"),
            ),),
            ui.column(
                9,
                ui.div(
                    {"class": "card"},
                    ui.h5({"class": "card-title m-0", "style": "font-weight: bold;text-align: center;"}, "Summarized Info"),
                    ui.output_table('genemaininfo'),
                ),
                ui.row(
                    ui.column(
                        6,
                        ui.div(
                            {"class": "card"},
                            ui.h5({"class": "card-title m-0", "style": "font-weight: bold;text-align: center;"},
                                  "House Keeping Gene Info"),
                            ui.output_table("hkgtable"),
                            style=table_style,
                        ),
                    ),
                    ui.column(
                        6,
                        ui.div(
                            {"class": "card"},
                            ui.h5({"class": "card-title m-0", "style": "font-weight: bold;text-align: center;"},
                                  "Tissue Specific Gene Info"),
                            ui.output_table("tstable"),
                            style=table_style,
                        ),
                    ),
                    ui.column(
                        12,
                        ui.div(
                            {"class": "card"},
                            ui.h5({"class": "card-title m-0", "style": "font-weight: bold; text-align: center;"},
                                  "Promoter Info"),
                            ui.output_table('promotertable'),
                        ),
                    ),
                    ui.column(
                        12,
                        ui.div(
                            {"class": "card"},
                            ui.h5({"class": "card-title m-0", "style": "font-weight: bold; text-align: center;"},
                                  "Select Expression Plot Options"),
                            ui.row(
                                ui.column(
                                4,
                                ui.input_radio_buttons("plot_order", "X-Axis Align", {"expression": "Expresison", "alphabetical": "Alphabetical"}),
                                ),
                                ui.column(
                                4,
                                ui.input_radio_buttons("plot_ylim", "Y-Axis Align", {"ab": "Absolute", "re": "Relative"}),
                                ),
                                ui.column(
                                4,
                                ui.input_radio_buttons("plot_db", "Database", {"geo": "GEO", "gtex": "GTEx","tcga" : "TCGA"}),
                                ),
                            ),
                        ),
                        ui.output_plot("expression_plot"),
                    ),
                ),
            ),
        ),
    ),
    ui.nav("Download",
           ui.row(
               ui.column(
                   12,
                   ui.div(
                       {"class": "card"},
                       ui.h5({"class": "card-title m-0", "style": "font-weight: bold; text-align: center;"},"Download Query Gene Set"),
                        ui.markdown("""
                                ##### Data Download
                                * All data are downloaded in TSV format. 
                                * After clicking the Run button, when the desired file name appears in the popup, please press Download.
                                </br>
                                ###### Tissue Specific Gene
                                * Check query tissue, multiple choice available.
                                * The TS score explains how tissue specific the gene is. To check the distribution, click on the box below.
                                * Consensus score represents how similarly the most highly expressed tissue is among 3 databases.
                                </br>
                                ###### House Keeping Gene
                                * CV, the coefficient of variation, has values between 0 and 1, and indicates the variation within each sample. Closer to 0 means less variation between samples.
                                * FC Pre-filtering is the fold change between the lowest and highest expressing tissues, which can be used for pre-filtering.
                                * Use the Consensus category to decide whether to get the intersection HKG candidate from three databases or the union HKG candidate.
                                </br>
                                ###### Up/Down Regulated Gene
                                * You can download genes where the value of query tissue / average expression value appears to be 4 times or more, and 0.25 times or less.
                                """),),
               ),
               ui.column(
                   4,
                   ui.div(
                       {"class": "card"},
                       ui.h5({"class": "card-title m-0", "style": "font-weight: bold;text-align: center;"},"Tissue Specific Gene"),
                       ui.input_selectize("tissue_checkbox","Check Query Tissue",tissue_selectize,multiple=True),
                       ui.input_slider("ts_score", "TS score", min=-1.525086, max=5.210999, value=1.5, step=0.01),
                       ui.input_slider("constitive_score","Consectutive Score",min=-0.833613,max=2.357001,value=1,step=0.01),
                       ui.input_slider("consensus","Consensus Percentile",min=0,max=1,value=0.6,step=0.1),
                       ui.input_action_button("ts_run", "Run"),
                       ui.output_text_verbatim("ts_download_run"),
                       ui.download_button("ts_download", "Download"),
                    ),
                ),
                ui.column(
                    4,
                    ui.div(
                        {"class": "card"},
                        ui.h5({"class": "card-title m-0", "style": "font-weight: bold;text-align: center;"},"House Keeping Gene"),
                        ui.input_slider('cv_percentile', "CV Percentile", min=0 , max=100, value=25, step=5),
                        ui.input_slider('hkg_fc',"FC pre-filtering",min=0, max=20, value=4, step=1),
                        ui.input_slider("constitive_score","Consectutive Score",min=-0.833613,max=2.357001,value=-0.833613,step=0.01),
                        ui.input_select("hkg_consensus", "Select Consensus", {"intersection": "Intersect Genes", "union": "Union Genes"}),
                        ui.input_action_button("hkg_run", "Run"),
                        ui.output_text_verbatim("hkg_download_run"),
                        ui.download_button("hkg_download", "Download"),
                    ),
                ),
                ui.column(
                    4,
                    ui.div(
                        {"class": "card"},
                        ui.h5({"class": "card-title m-0", "style": "font-weight: bold;text-align: center;"},
                                  "Up / Down Regulated Genes"),
                        ui.input_selectize("regulated_genes",
                                         "Check Query Tissue",
                                         tissue_selectize,
                                         multiple=True),
                        ui.input_select("up_or_down", "Select Up or Down", {"up": "Up Regulated", "down": "Down Regulated"}),
                        ui.input_action_button("regulate_run", "Run"),
                        ui.output_text_verbatim("regulate_download_run"),
                        ui.download_button("rgenes_download", "Download"),
                    ),
                ),
            ),
        ),
        ui.nav("Help",
               ui.div(
                   {"class": "card"},
                   ui.HTML(help_page)
                   ),),
    )

import json
with open(media + "/input/main_gene_info.json", "r") as file:
        main_info_dict = json.load(file)

def hyperlink(static, word):
    return ui.HTML("<A href = '{url}'>{name}</A>".format(url = static,name = word))

acceptable_input = {}
for k,v in symboldict.items():
    acceptable_input[k] = 0
    acceptable_input[v] = 0
for v in gene_input.values():
    acceptable_input[v] = 0

def plot_maker(gene, order, abre, db):
    file_path = media + '/barplots/' + db + '/' + gene + '.tsv'
    data = pd.read_csv(file_path, sep='\t', index_col=0)
    gene_name = gene
    gene_data = data.loc[gene_name]
    sorted_gene_data = gene_data.sort_index()
    if order == 'expression':
        sorted_gene_data = sorted_gene_data.sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sorted_gene_data.index, sorted_gene_data.values, color="blue")
    ax.set_title(f"Gene Expression for {gene_name}")
    ax.set_xlabel("Tissue")
    ax.set_ylabel("Expression (GeTMM)")
    ax.set_xticklabels(sorted_gene_data.index, rotation=45, ha="right")
    if abre == 'ab':
        ax.set_ylim(0, 2000)
    plt.tight_layout()
    return fig

class GenePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def create_kde_plot(self, data, label):
        self.kde_plot = sns.kdeplot(data, shade=True, label=label, ax=self.ax)

    def add_vertical_line(self, position, color='red', linestyle='--', label='Vertical Line'):
        self.ax.axvline(x=position, color=color, linestyle=linestyle, label=label)

def return_vline_table(gene, plot_object, parameter):
    file_path = media + "cv_ts_con_table.tsv"
    df = pd.read_csv(file_path, sep='\t')
    gene_dict = dict.fromkeys(df["Gene"])
    z_mean_data = df[parameter]
    if gene not in gene_dict.keys():
        if parameter == "CV":
            plot_object.ax.set_xlim(0, 20)
        plot_object.create_kde_plot(z_mean_data, 'Density Plot')
        return plot_object.fig
    plot_object.create_kde_plot(z_mean_data, 'Density Plot')
    gene_row = df[df['Gene'] == gene]
    if parameter == "TS":
        vertical_line_position = float(gene_row["TS"])
    elif parameter == "CV":
        plot_object.ax.set_xlim(0, 20)
        if float(gene_row["CV"]) > 20:
            verticla_line_position = 20
        else:
            vertical_line_position = float(gene_row["CV"])
    elif parameter == "Con":
        vertical_line_position = float(gene_row["Con"])
    plot_object.add_vertical_line(vertical_line_position)
    return plot_object.fig 


def server(input, output, session):
    @output
    @render.table
    def genemaininfo():
        gene = input.search_box()
        if gene not in acceptable_input.keys():
            return  
        answer = defaultdict(str)
        answer['Tissue'] = main_info_dict[gene]["Tissue"]
        answer['TS score'] = main_info_dict[gene]["TS score"]
        answer['Consecutive Score'] = main_info_dict[gene]['Constitive']
        answer['Up Regulated Tissue'] = ','.join(main_info_dict[gene]['Regulate']['Up'])
        answer['Down Regulated Tissue'] = ','.join(main_info_dict[gene]['Regulate']['Down'])
        answer['HKG'] = main_info_dict[gene]['HKG']
        df_answer = pd.DataFrame(answer,index= [0])
        return df_answer

    @output
    @render.table
    def hkgtable():
        gene = input.search_box()
        if gene not in acceptable_input.keys():
            return 
        root = media + 'dataframes/hkg/' + gene + '.tsv'
        answer = pd.read_csv(root, sep='\t')
        answer = answer.fillna('NA')
        return answer

    @output
    @render.table
    def tstable():
        gene = input.search_box()
        if gene not in acceptable_input.keys():
            return 
        root = media + 'dataframes/ts/' + gene + '.tsv'
        answer = pd.read_csv(root, sep = '\t')
        return answer

    @output
    @render.table
    def promotertable():
        gene = input.search_box()
        if gene not in acceptable_input.keys():
            return 
        root = media + 'dataframes/promoter/' + gene + '.tsv'
        answer = pd.read_csv(root, sep = '\t')
        return answer
    
    # TS button, run, download
    @reactive.Effect
    @reactive.event(input.ts_run)
    def _():
        global ts_root
        tissues = list(input.tissue_checkbox())
        tsscore = float(input.ts_score())
        constitive_score = float(input.constitive_score())
        consensus = float(input.consensus()) ##ts_download_parser(tissue, ts_score, consititive_score, consensus_percentile)
        answer = ts_download_parser(tissues, tsscore, constitive_score, consensus)
        ts_root = file_write(answer,"TS")

    @output
    @render.text
    @reactive.event(input.ts_run)
    def ts_download_run():
        filename = ts_root.split('/')[-1]
        return f"file name : {filename}"      

    @session.download()
    def ts_download():
        return ts_root
    
    # HKG button, run, download
    @reactive.Effect
    @reactive.event(input.hkg_run)
    def _():
        global hkg_root
        cv = float(input.cv_percentile())
        fc = float(input.hkg_fc())
        constitive = float(input.constitive_score())
        typo = input.hkg_consensus()  #hkg_download_parser(cv, fc, constitive, union)
        answer = hkg_download_parser(cv, fc, constitive, typo)
        hkg_root = file_write(answer,'hkg')
        
    
    @output
    @render.text
    @reactive.event(input.hkg_run)
    def hkg_download_run():
        filename = hkg_root.split('/')[-1]
        return f"file name : {filename}"
    
    @session.download()
    def hkg_download():
        return hkg_root

    # Regulate Button, run, download
    @reactive.Effect
    @reactive.event(input.regulate_run)
    def _():
        global regulate_root 
        regulate_root  = ''
        tissues = list(input.regulated_genes())
        upordown = input.up_or_down()
        answer = up_down_parser(tissues, upordown)
        regulate_root = file_write(answer,"Regulate")
    
    @output
    @render.text
    @reactive.event(input.regulate_run)
    def regulate_download_run():
        filename = regulate_root.split('/')[-1]
        return f"file name : {filename}"
    
    @session.download()
    def rgenes_download():
        return regulate_root
    
    @output
    @render.plot
    def expression_plot():
        gene = input.search_box()
        if gene not in acceptable_input.keys():
            return
        align = input.plot_order()
        ylim = input.plot_ylim()
        db = input.plot_db()
        return plot_maker(gene, align, ylim, db)

    @reactive.Effect
    @reactive.event(input.popup_geneset)
    def _():
        m = ui.modal(
            ui.markdown("""
                        * We serve 19,151 human protein coding genes.
                        * Tissue specificity (TS) and housekeeping gene (HKG) analyses are not provided for certain genes with extremely low expression levels.
                        * All gene matrix normalized with GeTMM
                        """),
           "Visit Help page for more detail description about parameter.",
            title="Geneset Description",
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)
    
    @reactive.Effect
    @reactive.event(input.popup_parameter)
    def _():
        m = ui.modal(
            ui.markdown("""
                        * **TS score** score quantifies the degree of high expression of a gene within a specific tissue, with values ranging from -1.5 to 5.2.
                        * **CV** is coefficient of variation, indicates the diversity within the distribution of samples, with values ranging from 0 to 1. A value closer to 0 suggests a more housekeeping-like pattern
                        * **Consecutive score** assesses the presence or absence of expression across numerous samples. It ranges from -0.8 to 2.35. 
                        * **Foldchange** in house keeping gene is the ratio of the average expression level in the tissue with the highest expression to the average expression level in the tissue with the lowest expression.
                        * **NFC** in tissue specific gene is the ration of the average expression level in the tissue with the highest expressionto the average expression level in the tissue with the second highest expression.
                        * Promoter informations obtained from EPD new
                        """),
            "Visit Help page for more detail description about parameter.",
            title="Parameter Description",
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)   
    
    @output
    @render.ui
    def gene_link():
        search = input.search_box()
        if search == 'Example':
            return ui.HTML("GeneCards Link   <A href = 'https://www.genecards.org/'>Example</A>")
        return ui.HTML("GeneCards Link   <A href='https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene}'>{Gene}</A>".format(gene = search, Gene = search))

    @reactive.Effect
    @reactive.event(input.popup_img_ts_score_distribution)
    def _():
        m = ui.modal(
            ui.output_plot("ts_score_img"),
            title="TS score Distribution",
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)  
    
    @output
    @render.plot
    def ts_score_img():
        gene = input.search_box()
        gene_plot = GenePlot()
        fig = return_vline_table(gene, gene_plot,"TS")
        return fig


    @reactive.Effect
    @reactive.event(input.popup_img_constitive_score_distribution)
    def _():
        m = ui.modal(
            ui.output_plot("con_score_img"),
            title="Consecutive score Distribution",
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)  
    
    @output
    @render.plot
    def con_score_img():
        gene = input.search_box()
        gene_plot = GenePlot()
        fig = return_vline_table(gene, gene_plot,"Con")
        return fig
    
    @reactive.Effect
    @reactive.event(input.popup_img_cv_distribution)
    def _():
        m = ui.modal(
            ui.output_plot("cv_img"),
            title="CV Distribution",
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)
    
    @output
    @render.plot
    def cv_img():
        gene = input.search_box()
        gene_plot = GenePlot()
        fig = return_vline_table(gene, gene_plot,"CV")
        return fig
    

app = App(app_ui,server)

