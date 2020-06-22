import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as pyplot
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


FILE_PATH = './data/Police_Department_Incident_Reports__2018_to_Present.csv';

# Non-violent crimes, or otherwise crimes that do not indicate an area is dangerous
IGNORED_CATEGORIES = [
  'Warrant',
  'Non-Criminal',
  'Lost Property',
  'Miscellaneous Investigation',
  'Other', #these appear to be death reports, accidental, natural causes, etc.
  'Recovered Vehicle',
  'Courtesy Report', #appears to be shit outside the jurisdiction that is ignored
  'Forgery And Counterfeiting',
  'Case Closure',
  'Suicide',
  'Fire Report',
  'Suspicious', #suspicious package
  'Vehicle Misplaced',
  'Gambling',
  'Missing Person', #not totally sure about this one
]

OTHER_CATEGORIES = ['Missing Person']

USED_CATEGORIES = [
  'Stolen Property',
  'Offences Against The Family And Children',
  'Larceny Theft',
  'Other Miscellaneous',
  'Assault',
  'Fraud', #not sure about this one
  'Burglary',
  'Traffic Violation Arrest', #this might be too minor, but maybe like drunk driving?
  'Weapons Carrying Etc',
  'Malicious Mischief',
  'Motor Vehicle Theft',
  'Drug Offense',
  'Other Offenses', #hodgepodge of stuff
  'Robbery',
  'Suspicious Occ',
  'Disorderly Conduct',
  'Weapons Offense',
  'Vandalism',
  'Embezzlement', #not sure about this one
  'Sex Offense',
  'Drug Violation', #Firearm, Armed While Possessing Controlled Substance
  'Traffic Collision', #includes hit and runs
  'Prostitution',
  'Homicide',
  'Arson',
  'Vehicle Impounded',
  'Liquor Laws',
  'Civil Sidewalks', #law that prevents people from sitting/lying on sidewalks between 7am-11pm
  'Family Offense',
  'Rape',
  'Weapons Offence', #typo with Weapons Offense?
  'Juvenile Offenses', #soliciting minor to commit felony
  'Human Trafficking, Commercial Sex Acts',
  'Human Trafficking (A), Commercial Sex Acts',
  'Motor Vehicle Theft?',
  'Human Trafficking (B), Involuntary Servitude', #there is only 1
]

# INCIDENT_CATEGORIES = ['Missing Person' 'Stolen Property' 'Non-Criminal' 'Lost Property'
#  'Miscellaneous Investigation' 'Offences Against The Family And Children'
#  'Larceny Theft' 'Other Miscellaneous' 'Warrant' 'Assault' 'Fraud'
#  'Burglary' 'Traffic Violation Arrest' 'Weapons Carrying Etc'
#  'Malicious Mischief' 'Motor Vehicle Theft' 'Drug Offense' 'Other'
#  'Other Offenses' 'Recovered Vehicle' 'Robbery' 'Suspicious Occ'
#  'Disorderly Conduct' 'Weapons Offense' 'Vandalism' 'Embezzlement'
#  'Courtesy Report' 'Sex Offense' 'Drug Violation' 'Traffic Collision'
#  'Prostitution' 'Forgery And Counterfeiting' 'Case Closure' 'Homicide'
#  'Arson' 'Suicide' 'Vehicle Impounded' 'Liquor Laws' 'Civil Sidewalks'
#  'Fire Report' 'Suspicious' 'Family Offense' 'Vehicle Misplaced' 'Rape'
#  nan 'Weapons Offence' 'Juvenile Offenses'
#  'Human Trafficking, Commercial Sex Acts'
#  'Human Trafficking (A), Commercial Sex Acts' 'Motor Vehicle Theft?'
#  'Gambling' 'Human Trafficking (B), Involuntary Servitude']

LON_RANGE = (-122.51129492624534, -122.36374276695295)
LAT_RANGE = (37.70798825918467, 37.82999075468864)

def trimNaN(df, col):
  return df.loc[~df[col].isna(), :]

def plotSeriesAsHist(ser):
  ser = ser[ser.notna()]
  unique_values = ser.unique()
  hist = {x: 0 for x in unique_values}
  for val in ser:
    hist[val] += 1

  pyplot.bar(hist.keys(), hist.values())
  pyplot.xticks(np.arange(0, len(unique_values)), unique_values, rotation=45, ha='right')
  pyplot.show()

def scatterPlot(df, xlabel, ylabel):
  print(crime_df.shape)

  pyplot.plot(xlabel, ylabel, 'o', data=crime_df)
  pyplot.xlabel(xlabel)
  pyplot.ylabel(ylabel)
  pyplot.axis('equal')
  pyplot.show()

def histogramBinsByLatLong(df, x1_label, x2_label, num_bins):
  x1 = df[x1_label]
  x2 = df[x2_label]

  x1_range = np.linspace(LON_RANGE[0], LON_RANGE[1], num_bins)
  x2_range = np.linspace(LAT_RANGE[0], LAT_RANGE[1], num_bins)

  grid = np.reshape(np.zeros(num_bins * num_bins), (num_bins, num_bins))

  for (i, row) in df.iterrows():
    x1_bin = x1_range[x1_range < row[x1_label]].shape[0] - 1
    x2_bin = x2_range[x2_range < row[x2_label]].shape[0] - 1
    grid[x1_bin][x2_bin] += 1

  return (grid, x1_range, x2_range)

#x1_label Longitude, x position
#x2_label latitude,  y position
def plotHeatmap(df, x1_label, x2_label, num_bins = 50):
  grid, x1_range, x2_range = histogramBinsByLatLong(df, x1_label, x2_label, num_bins)

  fig, ax = pyplot.subplots()
  ax.imshow(np.flip(grid, 0))
  ax.set_xticks(np.arange(num_bins))
  ax.set_yticks(np.arange(num_bins))
  ax.set_xticklabels(x1_range)
  ax.set_yticklabels(np.flip(x2_range, 0))
  fig.tight_layout()
  pyplot.show()


def twoDHistogram(df, x1_label, x2_label, num_bins = 50):
  grid, x1_range, x2_range = histogramBinsByLatLong(df, x1_label, x2_label, num_bins)

  fig = pyplot.figure()
  ax = fig.gca(projection='3d')

  X, Y = np.meshgrid(x1_range, x2_range)
  Z = grid

  # Plot the surface.
  surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

  # Customize the z axis.
  ax.zaxis.set_major_locator(LinearLocator(10))
  ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

  # Add a color bar which maps values to colors.
  fig.colorbar(surf, shrink=0.5, aspect=5)

  pyplot.show()


# Main
df = pd.read_csv(FILE_PATH)

print(df.shape)

crime_df = df.loc[df['Incident Category'].isin(USED_CATEGORIES),:]
# crime_df = df.loc[df['Incident Category'] == 'Drug Offense',:]

# scatterPlot(crime_df, 'Longitude', 'Latitude')
print(crime_df.shape)
crime_df = trimNaN(trimNaN(crime_df, 'Longitude'), 'Latitude')
print(crime_df.shape)

# plotHeatmap(crime_df, 'Longitude', 'Latitude')
twoDHistogram(crime_df, 'Longitude', 'Latitude')

# print(df['Incident Category'].unique())

# print(df.loc[df.loc[:,'Incident Category'] == 'Non-Criminal', ['Incident Subcategory', 'Incident Description']])
# category_ser = df.loc[df['Incident Category'] == 'Human Trafficking (B), Involuntary Servitude', 'Incident Description'];
# print(category_ser.unique())
# print(str(category_ser.shape[0]) + ': ' + str(category_ser.shape[0] / df.shape[0]))


# larceny_theft_df = df.loc[df.loc[:,'Incident Category'] == 'Larceny Theft', :]
# print(df.loc[df.loc[:,'Incident Category'] == 'Larceny Theft', 'Incident Description'].unique())



