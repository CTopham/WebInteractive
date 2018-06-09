import os
import json
import datetime as dt
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import pandas as pd
import pprint
import json
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request
    )

from flask_sqlalchemy import SQLAlchemy

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the sample and sample meta tables
otulist = Base.classes.samples
metameta = Base.classes.samples_metadata
otutax = Base.classes.otu
# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)


# #-------------------otu name table------------------------------------------
# class OTU(db.Model):
#    __tablename__ = 'otu'
#    otu_id = db.Column(db.Integer, primary_key=True)
#    lowest_taxonomic_unit_found = db.Column(db.String)

#    def __repr__(self):
#        return f"id={self.id}, name={self.name}"

# fetch('http://127.0.0.1:5000/names').then(data=>data.json()).then(rows => console.log(rows))

#--------------------------------------------------------------
@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

#--------------------------------------------------------------
@app.route('/otu')
def otu():
    result = {}

    results = session.query(otutax.lowest_taxonomic_unit_found).all()
    washlist = list(np.ravel(results))
    # for k,i in enumerate(results):
    #     # print(i)
    #     row = []
    #     innerRow ={}
    #     # print(i._asdict())
    #     for key in i._asdict():
            
    #         if(';' in i._asdict().get(key)):

    #             innerRes = i._asdict().get(key).split(';')
    #         else:
    #             innerRes = [i._asdict().get(key)]
            
    #         innerRow[key]=innerRes
    #         row.append(innerRow)
    #         result[str(k)] = row


    # print(result)
    return jsonify(washlist)

#--------------------------------------------------------------

@app.route("/names")
def names():
    results = [
        "940","941","943","944","945","946","947","948","949","950","952","953","954","955","956","958","959","960","961","962","963","964","966","967","968","969","970","971","972","973","974","975","978","1233","1234","1235","1236","1237","1238","1242","1243","1246","1253","1254","1258","1259","1260","1264","1265","1273","1275","1276","1277","1278","1279","1280","1281","1282","1283","1284","1285","1286","1287","1288","1289","1290","1291","1292","1293","1294","1295","1296","1297","1298","1308","1309","1310","1374","1415","1439","1441","1443","1486","1487","1489","1490","1491","1494","1495","1497","1499","1500","1501","1502","1503","1504","1505","1506","1507","1508","1510","1511","1512","1513","1514","1515","1516","1517","1518","1519","1521","1524","1526","1527","1530","1531","1532","1533","1534","1535","1536","1537","1539","1540","1541","1542","1543","1544","1545","1546","1547","1548","1549","1550","1551","1552","1553","1554","1555","1556","1557","1558","1561","1562","1563","1564","1572","1573","1574","1576","1577","1581","1601"
        ]
    #all_data = list(np.ravel(data))
    bbsample = [result[0:5] for result in results]
    return jsonify(results)
#--------------------------------------------------------------

@app.route("/wfreq")
def wash():
    results = session.query(metameta.WFREQ).\
    order_by(metameta.WFREQ).all()
    washlist = list(np.ravel(results))
    return jsonify(washlist)

@app.route("/wfreq/<sample>")
def washsample(sample = '940'):
    results = session.query(metameta.WFREQ).filter(metameta.SAMPLEID == sample).first()
    return jsonify(results)

@app.route("/metadata/<sample>")
def metaroute(sample = '940'):
    results = session.query(metameta.SAMPLEID, metameta.AGE, metameta.BBTYPE, metameta.ETHNICITY, metameta.GENDER, metameta.LOCATION).filter(metameta.SAMPLEID == sample).first()

    washlist = list(np.ravel(results))
    return jsonify(washlist)



@app.route("/names/<sample>")
def sampleit(sample = '940'):
    sample = "BB_" + sample

    csv_path = "DataSets/belly_button_biodiversity_samples.csv"
    df = pd.read_csv(csv_path, encoding="utf-8", dtype=object)
    df_sample = df[sample]
    df_sample = pd.DataFrame(list(df_sample))
    df_sample.rename(columns={0: 'Sample'}, inplace=True)
    df_sample[['Sample']] = df_sample[['Sample']].apply(pd.to_numeric)
    df_sample = df_sample.loc[df_sample["Sample"] > 0]
    df_sample = df_sample.sort_values('Sample', ascending=False)
    df_sample['otu_id'] = df_sample.index

    #df_sample.to_dict
    plot_trace = {
            "ID": df_sample['otu_id'].values.tolist(),
            "Sample": df_sample['Sample'].values.tolist()}
    #jsonfiles = json.loads(df_sample.to_json(orient='records'))
    return jsonify(plot_trace)
    

if __name__ == "__main__":
    app.run(debug=True)