# website reworked as a social discussion

This project is a modification of an [existing one](https://github.com/pythonlessons/Django_tutorials).

**Removed**.

application: newsletter.


**Added**.

applications: subscriptions and comments.

• subcategories.  
• subcategories related by categories.  
• you can subscribe to the communities you want.  
• home view shows your subscriptions and a category and subcategory filter.  
• you can comment on posts and reply to comments.  
• CRUD with django REST framework.  


**Changed**.

• home view shows posts.  
• posts are grouped by communities.  
• post creation is only enabled within a community and therefore inherits the community object automatically in the form.  
• posts inherit the categories and subcategories of the communities to which they belong automatically.  


note: this project needs more frontend work but this is only a practice in the backend side  
  note 1.1: i deployed this project on render.com and it works fine.










