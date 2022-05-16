### This are all the requiered libraries for the project

### install and import.

from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq



### it is the object of the flask framewwork basically we created our API with app as our variable name.
app = Flask(__name__)


@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI/web page

@cross_origin()


def index(): ### now we are defining a function called index that will do all the task as prescribed.

    if request.method == 'POST':

        try :

            searchString = request.form['content'].replace(" ", "")


            flipkart_url = "https://www.flipkart.com/search?q=" + searchString  ### this part is the url with the searchstring completing the url.
                                                                                 ### searchstring is basicaaly the name product u r trying to search

            uClient = uReq(flipkart_url)  ### uReq(flipkart) opens the url/link/website and uClient is the object of it.

            flipkartPage = uClient.read()  ### here a read operation is done of the page and flipkartPage is its object.

            uClient.close()

            flipkart_html = bs(flipkartPage,
                           "html.parser")  # bs is the alias for BeautifulSoup from bs4.trying to parse & beautify the info from page.
                                           # we are passing the url and parameter 'htmal.parser'
                                           # flipkart_html is its object

            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})   ## this part is trying to find all the division with all class signature with _1AtVbE col-12-12
                                                                                      ## and return all information in list form
                                                                                      ## bigboxes is its object.

            del bigboxes[0:3]                                     ## this part del first three element/info from bigboxes .
                                                                  # Maybe we do this because of structue  issue here its flipkart .
                                                                  ## This step may require vary between pages


            box = bigboxes[0]  ### here you get the first element or info from the object bigboxes.

            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']  ## we are reaching the href part in the multiple division.

            prodRes = requests.get(productLink)  ### we are getting the review info.

            prodRes.encoding = 'utf-8'  ### encoding is done 'utf-8' so that it is in english format.

            prod_html = bs(prodRes.text, "html.parser")  ## here we were able to parse the info and beautify.

            print(prod_html)

            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})  ### here we are reaching and finding all the comments box & returning it.

            filename = searchString + ".csv"  ## just creating a csv file with the search name as filename.

            fw = open(filename, "w")  # opening the csv file in write mode. so that all the info are saved in the csv file.

            headers = "Product, Customer Name, Rating, Heading, Comment \n"

            fw.write(headers)  ## this being the headers/column name of our csv file

            reviews = []  ## an empty list called review .later on to append mydict.

            for commentbox in commentboxes:  # running a for loop .means iterating through each multiple comments inside the commentboxes

                try:

                    # custComment.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text  ## extracting the name of the person commenting


                except:

                    name = 'No Name'  ##  exception handling if there is no name it will enlist as 'No name' in my mydict/csv file

                try:

                    # custComment.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text  ## extracting the rating giving by the person


                except:

                    rating = 'No Rating'  # exception handling if there is no rating it will enlist as 'No Rating' in my mydict/csv file

                try:

                    # custComment.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text  # extracting the heading of the comment giving by the person


                except:


                    commentHead = 'No Comment Heading'  # exception handling if there is no comment heading it will enlist as 'No Comment Heading' in my mydict/csv file

                try:

                    # custComment.encode(encoding='utf-8')
                    comtag = commentbox.div.div.find_all('div', {'class': ''})  # extracting the body of the comment/whole comment giving by the person


                    custComment = comtag[0].div.text


                except Exception as e:
                    print("Exception while creating dictionary: ",e)  # exception handling if there is no comment(body) it will enlist the  'Exception/error' in my mydict/csv file

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,"Comment": custComment}  ## the dictionary to store all the info in key-value pair
                                                                                                                                        # and then appendinding to list review.

                reviews.append(mydict)  # appending the dictationary mydict to review list

            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
                                                                              # ^ this tells the range go traverse through review.
                                                                              # assume len(reviews)=10,then 10-1=9 so the review=review[0:9]


        except Exception as e:

            print('The Exception message is: ', e)

            return 'something is wrong'
                     # return render_template('results.html')

    else:

          return render_template('index.html')


if __name__ == "__main__":
     #app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)




