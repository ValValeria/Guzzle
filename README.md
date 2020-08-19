![Image alt](https://github.com/ValValeria/Angular_Python/raw/master/tempsnip.png)

# Functionality
User can:
* sign up
* login
* add products to the shop list and see the quantity of each item
* go over products

# REST API 
* GET /search?search_query - finds an appropriate post
* GET /delcomment?comment_id - deletes the comment specified by comment_id
* GET /userposts/?user_id - find user's posts
* GET /deletepost/?user_id&post_id - delete user's post
* POST /update_post - update user's post
* GET /orderproducts/?user_id - get the orders of  user
* GET /addorderproducts/?user_id&post_id&num - add  orders to  user's list. If num equals 0 ,the product will be deleted from the user's list 
* GET /sortpost?sortBy&filter - sort posts by price. Allowed values of "sortBy" is 'priceDesc','priceBtw',"price"
* GET /category/cat_name - matches posts, which is related to the category, specified in cat_name  
* GET /catlist - gets the list of all categories
* GET /buyers/?post_id - gets the list of people who has bought the product specified in post_id
* GET /users/?page - gets the list of users. *Warning: the functionality is available only for the superuser*
* GET /deleteuser/?user_id - deletes the users. *Warning: the functionality is available only for the superuser*




