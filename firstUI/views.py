from django.shortcuts import render
import pandas as pd

def indexPage(request):
    confirmedGlobal = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        encoding='utf-8', na_values=None)
    totalcount=confirmedGlobal[confirmedGlobal.columns[-2]].sum()

    barplot = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-1]]].groupby(
        'Country/Region').sum().sort_values(by=confirmedGlobal.columns[-1], ascending=False).reset_index()
    barplot.columns = ['Country/Region', 'values']
    country = barplot['Country/Region'].tolist()
    values = barplot['values'].tolist()
    showMap='True'
    dataForMap=mapDataCal(barplot)

    context={'totalcount':totalcount,'country':country,'values':values,
             'dataForMap':dataForMap,'showMap':showMap}
    return render(request,'index.html',context)

def mapDataCal(barplot):
    df3 = pd.read_json(
        'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')

    df3['name'].replace(to_replace='United States', value='US', inplace=True)
    df3['name'].replace(to_replace='Russian Federation', value='Russia', inplace=True)
    df3['name'].replace(to_replace='Iran, Islamic Rep.', value='Iran', inplace=True)
    df3['name'].replace(to_replace='Egypt, Arab Rep.', value='Egypt', inplace=True)
    df3['name'].replace(to_replace='Iran, Islamic Rep.', value='Iran', inplace=True)
    df3['name'].replace(to_replace='Korea, Rep.', value='Korea, South', inplace=True)
    df3['name'].replace(to_replace='Venezuela, RB', value='Venezuela', inplace=True)

    js_df = df3.merge(barplot, right_on='Country/Region', left_on='name')
    dataForMap = []
    for i in range(len(js_df)):
        try:

            temp = {}
            temp['code3'] = js_df[i:i + 1]['code3'].values[0]
            temp['name'] = js_df[i:i + 1]['Country/Region'].values[0]
            temp['value'] = js_df[i:i + 1]['values'].values[0]
            temp['code'] = js_df[i:i + 1]['code'].values[0]
            dataForMap.append(temp)
        except:
            pass

    return dataForMap

def IndiCountryData(request):
    countryNameSe=request.POST.get('countryName')
    confirmedGlobal = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        encoding='utf-8', na_values=None)
    totalcount = confirmedGlobal[confirmedGlobal.columns[-2]].sum()

    barplot = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-1]]].groupby(
        'Country/Region').sum().sort_values(by=confirmedGlobal.columns[-1], ascending=False).reset_index()
    barplot.columns = ['Country/Region', 'values']
    country = barplot['Country/Region'].tolist()
    values = barplot['values'].tolist()
    showMap='False'

    countryDataSpe = pd.DataFrame(confirmedGlobal[confirmedGlobal['Country/Region'] == countryNameSe][
                                      confirmedGlobal.columns[4:-1]].sum()).reset_index()
    countryDataSpe.columns = ['country', 'values']
    countryDataSpe['lagVal'] = countryDataSpe['values'].shift(1).fillna(0)
    countryDataSpe['incrementVal'] = countryDataSpe['values'] - countryDataSpe['lagVal']
    countryDataSpe['rollingMean'] = countryDataSpe['incrementVal'].rolling(window=4).mean()
    countryDataSpe = countryDataSpe.fillna(0)
    datasetsForLine = [
        {'yAxisID': 'y-axis-1', 'label': 'Daily Cumulated Data', 'data': countryDataSpe['values'].values.tolist(),
         'borderColor': '#03a9fc', 'backgroundColor': '#03a9fc', 'fill': 'false'},
        {'yAxisID': 'y-axis-2', 'label': 'Rolling Mean 4 days', 'data': countryDataSpe['rollingMean'].values.tolist(),
         'borderColor': '#fc5203', 'backgroundColor': '#fc5203', 'fill': 'false'}]
    axisvalues=countryDataSpe.index.tolist()
    context = {'axisvalues':axisvalues,'countryName':countryNameSe,'totalcount': totalcount, 'country': country, 'values': values,
               'showMap':showMap,'datasetsForLine':datasetsForLine}
    return render(request, 'index.html', context)