# Mission-to-Mars-Challenge
Creating a polished portfolio of Mars news and images for research purposes.

# Purpose
The purpose of this mission was to explore Mars using the internet. The python application file uses four different websites to collect various information and graphics. It then utilizes BeautifulSoup and Flask to generate a polished website with all the results. It also contains an interactive button should more current data or information be requested.

# Analysis
The first website checked for the latest headlines regarding Mars was https://redplanetscience.com/. Using the code, it was possible to scrape the first parent element to find the first tag, listed under class  `content_title` and save it as `news_title`. Subsequently, the associated parapraph for this news title was also captured and placed under the title. This section is continuously updated by pressing the `Scrape New Data` button.

Next, the latest featured image of Mars is pulled from the website https://spaceimages-mars.com using the same methodology as noted above except now looking for the `img` tag. The source of this image was extracted and placed in the same row as the Mars Facts table. The Mars facts table was pulled from https://galaxyfacts-mars.com. This data was read from html, converted to a Pandas dataframe, then re-converted back to an HTML table. The tricky part with using Bootstrap on a Dataframe is that the classes need to be added in the .py code instead of the HTML code if not using the `table` tags.

The last site to visit included obtaining images of the four hemispheres of Mars from the website https://marshemispheres.com/. From this site, an iterative process was created to click into each of the four links, extract the caption and photo, and then return back to the main page to go on to the next hemisphere. This information was then placed underneath the featured image and facts table as a row of thumnails within the HTML code.

After all that, the resulting website rendering is shown below:

![Mars_Website](Images\Mission_to_Mars_Site.PNG)
