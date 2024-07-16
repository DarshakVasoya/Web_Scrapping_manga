# importing files
import main_page_scrapper

# Headers to include in the request to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}




# for demo purpose
# page_url = "https://manhuatop.org/manhua/page/3/?m_orderby=new-manga"
# main_page_scrapper.page_scrap(page_url,headers)


# for scrapping whole website

i=1
while True:
    page_url = "https://manhuatop.org/manhua/page/"+str(i)+"/?m_orderby=new-manga"
    main_page_scrapper.page_scrap(page_url,headers=headers)
    print(i)
    ans=input("you want to continue answer : yes or no::")
    if ans=="no":
        break
    i=i+1