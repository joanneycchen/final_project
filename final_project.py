#################################
##### Name: Joanne
##### Uniqname: joanneyc
#################################

from bs4 import BeautifulSoup
import requests
import json
import time
import secrets  # file that contains your API key
import plotly.graph_objs as goooo
import sqlite3






baseurl = 'https://api.yelp.com/v3/businesses/search'
CACHE_FILE_NAME = 'statecities.json'
CACHE_DICT = {}
headers = {'User-Agent': 'python-requests/2.25.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
API_KEY = secrets.API_KEY






def load_cache():
    ''' opens the cache file if it exists and loads the JSON into the FIB_CACHE dictionary.    
    if the cache file doesn't exist, creates a new cache dictionary    
    Parameters    
    ----------    
    None    
    Returns   
     -------    
     The opened cache
   
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache: dict
    The dictionary to save
    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    ''' 
    check if the url is in the cache, if there is cache, use cache
    if there is no cache,  fetch the data

    Parameters
    ----------
    url
    cache: dict

    Returns
    -------
    cache dic
    '''
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        # print(cache.keys())

        return cache[url] # return the dic key
    else:
        print("Fetching")
        # print(cache.keys())
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from wikipedia and worldpopulationreview

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''


    state_url='https://en.wikipedia.org/wiki/Category:Lists_of_cities_in_the_United_States_by_state'
    CACHE_DICT = load_cache()
    responseDetail = make_url_request_using_cache(state_url, CACHE_DICT)
    soup = BeautifulSoup(responseDetail, 'html.parser')
    listing_parent = soup.find(class_='navbox-list navbox-odd')
    listing_state = listing_parent.find_all('li')

    state_dic = {}
    for state in listing_state:
   
        state_name = state.find('a')
        name = state_name.text.strip().lower().replace(" ", "-")

        
   
        whole_url = 'https://worldpopulationreview.com/states/cities/'+name


        state_dic[state_name.text.strip().lower()] = whole_url

    return state_dic


def get_cities_for_state(state_url):
    '''Make a list of top 10 cities from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in worldpopulationreview.com
    
    Returns
    -------
    list
        10 top cities in the state

    '''
    CACHE_DICT = load_cache()
    responseDetail = make_url_request_using_cache(state_url, CACHE_DICT)
    soup = BeautifulSoup(responseDetail, 'html.parser')

    each_np_divs = soup.find('div', class_='row')
    list_cities = each_np_divs.find('ul')
    cities =[]
    for city in list_cities:
        name = city.find('a').text.strip()
   
        cities.append(name)

    return cities



def get_nearby_restaurant(location):
    '''Obtain API data from Yelp API.
    
    Parameters
    ----------
    location: object
        an instance of a city
    
    Returns
    -------
    dict
        a converted API return from Yelp API
    '''

    baseurl = 'https://api.yelp.com/v3/businesses/search'

    headers = {
    'Authorization': f'bearer %s' % API_KEY,
    }
    params = {
        'term':'restaurants',
        'limit':20,
        'radius': 10000,
        'location': location
    }

    response = requests.get(baseurl, headers=headers, params=params)
    data = response.json()


    number=0

    name_list=[]
    rating_list=[]
    address_list=[]
  
    city_list=[]
    zipcode_list=[]

    one_perlocation_list=[]
    two_perlocation_list=[]
    
    # dic_restaurant={}
    # dic_category={}
    
    for each in data['businesses']:
        # print('each',each)
        tableone_location_restaurant=[]
        tabletwo_location_restaurant=[]
        list_of_categories=[]     
        number+=1
        city= each['location']['city']
        zipcode= each['location']['zip_code']
        name = each['name']
        categories = each['categories']
        rating = each['rating']
        address = each['location']['display_address'][0]

        
        name_list.append(name)
        rating_list.append(rating)
        address_list.append(address)
        city_list.append(city)
        zipcode_list.append(zipcode)
        # list_of_categories.append(categories)
        # print(city_list)
        # print('categories', categories)

        for each_category in categories:
            list_of_categories.append(each_category['title'])
   
        #make the restuaurant info to a list 
        tableone_location_restaurant.append(name)
        tableone_location_restaurant.append(location)
        tableone_location_restaurant.append(rating)
        # tableone_location_restaurant.append(address)
        # tableone_location_restaurant.append(str(list_of_categories))
        # print('location_restaurant', tableone_location_restaurant)
        # category_list.append(list_of_categories)

        tabletwo_location_restaurant.append(name)
        tabletwo_location_restaurant.append(address)
        tabletwo_location_restaurant.append(str(list_of_categories))



        one_perlocation_list.append(tableone_location_restaurant)
        two_perlocation_list.append(tabletwo_location_restaurant)
        # print('one_perlocation_list', one_perlocation_list)
        # print('two_perlocation_list', two_perlocation_list)

    #individual resturant with different name, rating, address, categories but added all tgt to a list
    #table1
    # dic_restaurant['name']=name_list
    # dic_restaurant['rating']=rating_list
    # #table2
    # dic_category['name']=name_list
    # dic_category['address']=address_list
    # # dic_restaurant['city']=location
    # dic_category['category']=category_list
    

  
    # # print('dic_category', dic_category)
    # # print('dic_restaurant', dic_restaurant)
    # print('perlocation_list', perlocation_list)

    # return dic_restaurant, dic_category, perlocation_list
    return one_perlocation_list, two_perlocation_list

def create_data():
    '''Creating database and table if not existed. If existed, drop the table

    Parameters
    ----------
    location: object
        an instance of a city
    
    Returns
    -------
    None
    '''
    conn = sqlite3.connect("./restaurantlist.sqlite") 
    cur = conn.cursor()
    drop_teams = '''    DROP TABLE IF EXISTS "restaurants";'''
    create_list = '''
    CREATE TABLE IF NOT EXISTS "restaurants"(
        "Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Name" TEXT NOT NULL,
        "City" TEXT NOT NULL,
        "Rating" REAL NOT NULL
    );
    '''

    cur.execute(drop_teams)
    cur.execute(create_list)

    drop_teams2 = '''    DROP TABLE IF EXISTS "category";'''
    create_list2 = '''
    CREATE TABLE IF NOT EXISTS "category"(
        "Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Name" TEXT NOT NULL,
        "Address" TEXT NOT NULL,
        "Category" TEXT NOT NULL
    );
    '''
    cur.execute(drop_teams)
    cur.execute(create_list)

    cur.execute(drop_teams2)
    cur.execute(create_list2)
    
    conn.commit() 




def update_data(tablename, perlocation_list):
    '''getting data from database and converted into a dictoinary

    Parameters
    ----------
    location_name: table name
    perlocation_list: the resturant information from the city 
    
    Returns
    -------
    None
    '''

    conn = sqlite3.connect("./restaurantlist.sqlite") 
    cur = conn.cursor()
    table_name = tablename
    one_insert_team = f"INSERT INTO {table_name} VALUEs (NULL,?,?,?)"
    # two_insert_team = f"INSERT INTO {table_name} VALUEs (NULL,?,?,?)"
    
    for each_restaurant in perlocation_list:
        # print('each_restaurant', each_restaurant)
        cur.execute(one_insert_team, each_restaurant)
        conn.commit() 

    # for each_restaurant in perlocation_list:
    #     # print('each_restaurant', each_restaurant)
    #     cur.execute(two_insert_team, each_restaurant)
    #     conn.commit() 

def check_data_base(city_name, database_list, one_perlocation_list, two_perlocation_list):
    '''check if the city relatated restaurant data is inside the database. 
    If not, insert the data. If it is, get the data from the database
    in the end comnbine the data

    Parameters
    ----------
    city_name: city name
    database_list: the list of data that are already in the database 
 
    Returns
    -------
    dic_to_restaurant: the dictionary of the restaurant info
    database_list: updated data list 

    '''
    # print('check database')

    if city_name not in database_list:
        update_data('category', two_perlocation_list)
        update_data('restaurants', one_perlocation_list)
        database_list.append(city_name)
        print('Inserting data to database =======================================================')
        conn = sqlite3.connect("./restaurantlist.sqlite")
        cur = conn.cursor()
        q4 = f'SELECT * FROM restaurants WHERE City="{city_name}"'
        cur.execute(q4)
        # dic_to_restaurant = fetch_data_todic(cur)
        conn.close()

    else:
        print('fetching from database =======================================================')
        conn = sqlite3.connect("./restaurantlist.sqlite")
        cur = conn.cursor()
        q4 = f'SELECT * FROM restaurants WHERE City="{city_name}"'
        cur.execute(q4)
        # dic_to_restaurant = fetch_data_todic(cur)
        conn.close()
    
    conn = sqlite3.connect("./restaurantlist.sqlite")
    cur = conn.cursor()
    q3 = f'SELECT * FROM restaurants JOIN category ON restaurants.Name=category.Name WHERE City="{city_name}"'
    cur.execute(q3)
    dic_to_restaurant = fetch_data_todic(cur)
    conn.close()

    # "SELECT * FROM restaurants JOIN category ON restaurants.Name=category.Name"

    return dic_to_restaurant, database_list


def fetch_data_todic(cur):
    '''getting data from database and converted into a dictoinary to create plot

    Parameters
    ----------
    cur: data from the table
    
    Returns
    -------
    dict
        a dictionary from the database
    '''
 
    name_list=[]
    rating_list=[]
    city_list=[]
    address_list=[]
    category_list=[]
    dic_restaurant={}
    for row in cur:
   
        name_list.append(row[1])
        city_list.append(row[2])
        rating_list.append(row[3])
        address_list.append(row[6])
        category_list.append(row[7])
    dic_restaurant['name'] = name_list
    dic_restaurant['rating'] = rating_list
    dic_restaurant['city'] = city_list
    dic_restaurant['address'] = address_list
    dic_restaurant['category'] = category_list
    # print('dic_restaurant123', dic_restaurant)
    return dic_restaurant



def show_table(dic_restaurant):
    '''transfer the dictionary to display into a table 

    Parameters
    ----------
    dic_restaurant: dictionary of the resutaurant info
 
    Returns
    -------
    None
    '''


    name_list = dic_restaurant['name']
    rating_list = dic_restaurant['rating']
    city_list = dic_restaurant['city']
    address_list = dic_restaurant['address']
    category_list = dic_restaurant['category']


    fig = goooo.Figure(data=[goooo.Table(header=dict(values=['Name', 'City', 'Rating', 'Category', 'Address']),
                 cells=dict(values=[name_list, city_list, rating_list, category_list, address_list]))
                     ])
    fig.show()
    


def show_rador_chart(dic_restaurant):
    '''transfer the dictionary to display into a radar chart based on resturant name and rating 

    Parameters
    ----------
    dic_restaurant: dictionary of the resutaurant info
 
    Returns
    -------
    None
    '''
    rating_list = dic_restaurant['rating']
    name_list = dic_restaurant['name']
    fig = goooo.Figure(data=goooo.Scatterpolar(
    r=rating_list,
    theta=name_list,
    fill='toself'
    ))

    fig.update_layout(
    polar=dict(
    radialaxis=dict(
        visible=True
    ),
    ),
    showlegend=False
    )

    fig.show()
    return




if __name__ == "__main__":
    all_the_states = build_state_url_dict()
    # print(all_the_states)
    create_data()
    database_list=[]
    while True:
        # create_category_data()
        state_name = input('Enter a state name (e.g. Michigan, michigan) that you want to visit or "exit" ')
        if state_name.lower()=='exit':
            quit()
        elif state_name.lower() not in all_the_states.keys():
            print('[Error] Enter proper state name ')
            pass
        else:
            answer = ""
            number = 0
            print('---------------------------------')
            print(f"Theese are the top 10 cities in {state_name.lower()}")
            print('---------------------------------')
            state = state_name.lower()
            state_url = all_the_states[state]
            sites = get_cities_for_state(state_url)
        
            for site in sites:
                number+=1
                each_site =  f"[{number}] {site}"
                print(each_site) #to let user to choose option (need to include)
            
            while answer != 'exit' or answer != 'back':
                answer = input('Choose a number for detail search or "exit" or "back" ')
          
                if answer.isnumeric() and 1 <= int(answer) <= len(sites):
                    i = int(answer)-1
                    city_name = sites[i]
                    # dic_restaurant, dic_category, perlocation_list = get_nearby_places(city_name)
                    one_perlocation_list, two_perlocation_list = get_nearby_restaurant(city_name)
                    # print('dic_restaurant', dic_restaurant)
                    # print('-----------------------------------------------')
                    # print('perlocation_list', perlocation_list)
                    # update_list=dic_restaurant['update_list']
                    dic_to_restaurant, database_list = check_data_base(city_name, database_list, one_perlocation_list, two_perlocation_list)
                    # print('dic_to_restaurant', dic_to_restaurant)
                    # fetch_data_todic(cur)
                    
                    # print('database_list', database_list)
                    chart_answer = input('Would you want to see the radar chart and the table? ')
                    if chart_answer.lower()=='yes':
                        print('yes')
                        show_table(dic_to_restaurant)
                        show_rador_chart(dic_to_restaurant)                       
                    else:
                        break

                elif answer == 'exit':
                    exit()
                elif answer.isnumeric() and 1 > int(answer):
                    print('[Error] Invalid input')
                elif answer.lower()!='back':
                    print('[Error] Invalid input')
                else:
                    answer = 'back'
                    print(answer)
                    break