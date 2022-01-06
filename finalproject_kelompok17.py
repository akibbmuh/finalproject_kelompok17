# -*- coding: utf-8 -*-
"""FinalProject_Kelompok17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GvBzuukNQgsn4PlrR5ucPCPk34Vncqhi

## Kelompok 17
######Muh. Akib A. Yani (1301194233)
######Putri Samapa Hutapea (1301190336)
######Zahra Fadiah Putri (1301194212)
## IF-42-GAB06
"""

#Library yang digunakan
import time
import pandas as pd
import numpy as np

from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_notebook, push_notebook, output_file
from bokeh.transform import linear_cmap
from bokeh.models import ColumnDataSource, HoverTool

from bokeh.tile_providers import get_provider, Vendors
from pyproj import Proj, transform

from bokeh.layouts import row, column, grid, gridplot
from bokeh.models import CustomJS
from bokeh.models.widgets import Button, Select

output_file("tubes.html")

iSelect=0           # Index Select
nSum = [0,0,0,0,0,0,0]
nMinMax = [0,0,0,0,0,0,0]

#Dataset
df1=pd.read_csv('https://raw.githubusercontent.com/valiandafh/Tubes-/master/time_series_covid19_confirmed_global.csv')    # Confirmed
df2=pd.read_csv('https://raw.githubusercontent.com/valiandafh/Tubes-/master/time_series_covid19_recovered_global.csv')    # Recovered
df3=pd.read_csv('https://raw.githubusercontent.com/valiandafh/Tubes-/master/time_series_covid19_death_global.csv')        # Death

df1.rename(columns={'Province/State':'Province', 'Country/Region':'Country'}, inplace=True)
maxBaris=len(df1.iloc[:,0])     # 264baris
maxKolom=len(df1.iloc[0,:])     # 96kolom

df1['Total'] = df1.iloc[:,-1]
df2['Total'] = df2.iloc[:,-1]
df3['Total'] = df3.iloc[:,-1]

dCountry=df1['Country']
dProvince=df1['Province']
lCountry=dCountry.values.tolist()
lProvince=dProvince.values.tolist()

# List of Select
L1 = lCountry
L2 = lProvince
L3 = L1

y1=df1.iloc[iSelect,4:maxKolom]
y2=df2.iloc[iSelect,4:maxKolom]
y3=df3.iloc[iSelect,4:maxKolom]
x1=[x1 for x1 in range(0,len(y1))]
mydates=y2.index.values
nBaris=len(lCountry)-1
nKolom=len(x1)-1

#Button
mybtn15 = Button(label="Confirmed = 1176", name="12", width=120)
mybtn16 = Button(label="Recovered = 166", name="12", width=120)
mybtn17 = Button(label="Death = 140", name="12", width=120)

#Peta dan Data
mydf=df1
mytitle="Visualisasi Statistik COVID-19"
x=mydf['Long']
y=mydf['Lat']
z=mydf['Total']
myC=mydf['Country']

mysizes=np.abs(z)
myWarna=np.abs(z)

# Konversi WGS84 to Mercator
in_wgs = Proj('epsg:4326')
out_mercator = Proj('epsg:3857')

mX = np.abs(x)
mY = np.abs(y)
for ii in range(len(x)):
  mX[ii], mY[ii] = transform(in_wgs, out_mercator, y[ii], x[ii])

  nMin=5000000
nMax=0
iMin=0
iMax=0
for ii in range(len(z)):
  if (z[ii]>nMax):
    nMax=z[ii]
    iMax=ii

for ii in range(len(z)):
  if (z[ii]<nMin):
    if (z[ii]>0):
      nMin=z[ii]
      iMin=ii

# Size of Circle
for ii in range(len(z)):
  mysizes[ii]=(5 if (z[ii]<1000) else 
              (10 if z[ii]<10000 else 
              (16 if z[ii]<100000 else 
              (28 if z[ii]<500000 else 
              42))))

for ii in range(len(z)):
  myWarna[ii]=(0 if (z[ii]<10) else 
              (1 if z[ii]<100 else 
              (3 if z[ii]<1000 else 
              (5 if z[ii]<10000 else 
              (7 if z[ii]<100000 else 
              (9 if z[ii]<500000 else 
              12))))))

for ii in range(len(z)):
  if (z[ii]<100): nSum[0]=nSum[0]+1 
  elif (z[ii]<1000): nSum[1]=nSum[1]+1
  elif (z[ii]<10000): nSum[2]=nSum[2]+1
  elif (z[ii]<100000): nSum[3]=nSum[3]+1
  elif (z[ii]<500000): nSum[4]=nSum[4]+1
  else: nSum[5]=nSum[5]+1 
nSum[6]=len(z)

#MinMax
nMinMax[0]=iMin
nMinMax[1]=nMin
nMinMax[2]=iMax
nMinMax[3]=nMax

mydf['E']=mX
mydf['N']=mY
mydf['Size'] = mysizes
mydf['Warna'] = myWarna

myfillcolors = linear_cmap(field_name='Warna', palette='Spectral6', low=min(myWarna), high=max(myWarna))

mysource = ColumnDataSource(mydf)
myhover = HoverTool(tooltips=[("Country ", "@Country"), 
                              ("Province ", "@Province"),
                              ("Long ", "@Long"),
                              ("Lat ", "@Lat"),
                              ("Total ", "@Total")])

# range bounds supplied in web mercator coordinates
M1 = figure (plot_width=600, plot_height=440,
  x_range=(-16000000, 16000000), y_range=(-8000000, 8000000),
  x_axis_type='mercator', y_axis_type='mercator',
  title=mytitle, tools=[myhover, 'pan', 'wheel_zoom', 'zoom_in', 'zoom_out','save', 'reset']
)

# tile_provider = get_provider(Vendors.STAMEN_TONER_BACKGROUND)
mytile_provider = get_provider(Vendors.CARTODBPOSITRON)

mybtn21 = Button(label="Min : ", width=250)
mybtn22 = Button(label="Click here", width=90)
mybtn23 = Button(label="Max : ", width=250)

def myhandler2b():
  i=nMinMax[0]
  mybtn21.label = L1[i]+" = "+str(z[i])+", "+str(df2['Total'][i])+", "+str(df3['Total'][i])
  i=nMinMax[2]
  mybtn23.label = L1[i]+" = "+str(z[i])+", "+str(df2['Total'][i])+", "+str(df3['Total'][i])
  
mybtn22.on_click(myhandler2b)

B22 = row(mybtn21, mybtn22, mybtn23)

#Pembuatan Slider
iSlider = nKolom      # Index of Slider (0-91 days)

x1c = x1
y1c = df1.iloc[iSelect,4:maxKolom]
y2c = df2.iloc[iSelect,4:maxKolom]
y3c = df3.iloc[iSelect,4:maxKolom]

x1d=[x1 for x1 in range(0,len(y1))]
y1d=[x1 for x1 in range(0,len(y1))]
y2d=[x1 for x1 in range(0,len(y1))]
y3d=[x1 for x1 in range(0,len(y1))]

def PDailyCase(iNum):
  for i in range(1, nKolom):
    y1d[i]=y1c[i]-y1c[i-1]
    y2d[i]=y2c[i]-y2c[i-1]
    y3d[i]=y3c[i]-y3c[i-1]

PDailyCase(iSelect)

mybtn31 = Button(label=mydates[nKolom], width=70)
mybtn32 = Button(label=str(y1d[nKolom]), width=70)
mybtn33 = Button(label=str(y2d[nKolom]), width=50)
mybtn34 = Button(label=str(y3d[nKolom]), width=50)

source3 = ColumnDataSource(data=dict(x1c=x1c, y1c=y1c, y2c=y2c, y3c=y3c))
source3b = ColumnDataSource(data=dict(x1d=x1d, y1d=y1d, y2d=y2d, y3d=y3d))

#pemberian judul
plot3 = figure(plot_width=300, plot_height=200, title="Akumulasi Laporan", toolbar_location=None)
plot3.x_range.start = 0
plot3.y_range.start = 0

plot3b = figure(plot_width=300, plot_height=200, title="Laporan Kasus Harian", toolbar_location=None)
plot3b.x_range.start = 0
plot3b.y_range.start = 0

#pemberian warna
r1 = plotx.line('x1c', 'y1c', source=sourcex, line_width=3, line_color='red', legend_label='confirmed')
r2 = plotx.line('x1c', 'y2c', source=sourcex, line_width=3, line_color='green', legend_label='recovered')
r3 = plotx.line('x1c', 'y3c', source=sourcex, line_width=3, line_color='blue', legend_label='death')

r1b = ploty.line('x1d', 'y1d', source=sourcey, line_width=3, line_color='red', legend_label='confirmed')
r2b = ploty.line('x1d', 'y2d', source=sourcey, line_width=3, line_color='green', legend_label='recovered')
r3b = ploty.line('x1d', 'y3d', source=sourcey, line_width=3, line_color='blue', legend_label='death')

# Cek NaN variable (Variabel Kosong)
def isNaN(num):
  return num!= num

for i in range(nBaris):
  L3[i]=(L1[i] if isNaN(L2[i]) else (L1[i]+L2[i]))

def myhandler3a(attr,old,new):
  iSelect=-1
  for i in range(0, nBaris):
    iSelect=(i if (L1[i]==new) else iSelect) 

  mybtn31.label = mydates[nKolom]
  y3c = df3.iloc[iSelect,4:maxKolom]
  y2c = df2.iloc[iSelect,4:maxKolom]
  y1c = df1.iloc[iSelect,4:maxKolom]
  mybtn15.label = "Confirmed = " + str(y1c[nKolom])
  mybtn16.label = "Recovered = " + str(y2c[nKolom])
  mybtn17.label = "Death = " + str(y3c[nKolom])
  r1.data_source.data["y1c"] = y1c
  r2.data_source.data["y2c"] = y2c
  r3.data_source.data["y3c"] = y3c

  for i in range(1, nKolom+1):
    y1d[i]=y1c[i]-y1c[i-1]
    y2d[i]=y2c[i]-y2c[i-1]
    y3d[i]=y3c[i]-y3c[i-1]
  r1b.data_source.data["y1d"] = y1d
  r2b.data_source.data["y2d"] = y2d
  r3b.data_source.data["y3d"] = y3d
  mybtn32.label = str(y1d[nKolom])
  mybtn33.label = str(y2d[nKolom])
  mybtn34.label = str(y3d[nKolom])

opsiSelect=L3
myselect3 = Select(value=opsiSelect[0], options=opsiSelect, title="Country/Province ", width=150)
myselect3.on_change('value', myhandler3a)

print(nBaris) 
print(nKolom)
print(L1[nBaris])
print(y1c[nKolom])
print(y2c[nKolom])
print(y3c[nKolom])

A = column(myselect3, mybtn15, mybtn16, mybtn17)

C33 = row(mybtn31, mybtn32, mybtn33, mybtn34)
C = column(plot3, C33, plot3b)

MyLayout = row(A, C)
#show(MyLayout)
curdoc().add_root(MyLayout)
curdoc().title = "Visualisasi Statistik COVID-19"