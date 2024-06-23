# File Handling Project Documentation

## Certificate of Completion
This document certifies that the Online Food Ordering System Project has been completed successfully. All required functionalities
have been implemented and tested.

## Acknowledgement

We would like to express our sincere gratitude to Aptech for entrusting us with the opportunity to develop this Online Food System. This project allowed us to leverage our skills and expertise to create a digital platform that aligns with project's mission of providing top-quality culinary services.. We would also like to extend our heartfelt thanks to Mr. Obed Jonathan & Mr Emmanuel Odedele, whose invaluable guidance and support played a pivotal role in the successful completion of this project. We are also grateful to our peers and the technical staff at Aptech,Alagbole for their assistance and encouragement. This project would not have been possible  without the collaborative effort and shared insights of everyone involved.

## Project Synopsis

The Online Food Ordering System is an e-commerce solution that enables restaurants to upload menus online, attract potential customers, and increase sales. This system allows customers to place orders online 24/7, providing a convenient and fast food ordering experience. By adopting this system, restaurants can expand their business, gain a competitive edge, and enjoy increased sales at an affordable price.

## Table of Contents

1. Problem Definition
2. Customer Requirement Specification
3. Project Plan
4. ER Diagram
5. Algorithms
6. Task Sheet
7. Project Review and Monitoring Report
8. Project Analysis
9. Project Design
10. GUI Standard Doc
11. Interface Design Doc
12. Database Structure
13. Screen Shots
14. Source Codes with Comments
15. User Guide
16. Developers Guide-Module Description
17. Final Check List
18. Conclusion
19. Developers Information

## Problem Definition

The problem is to design and develop an online food ordering system that allows customers to browse menus, place orders, and make payments online.

## Customer Requirement Specification
## The customer requires the following features:
- User registration and login;
- Menu browsing and searching;
- Order placement and payment processing;
- Order history and tracking;
- Admin dashboard for managing orders, users, and menu items.

## Project Plan
- Day1: Project Planning and Requirements Gathering;
- Day2-3: Database Design and Development(Using Django);
- Day4-5: Frontend Development(Using Html,C,ss & JS);
- Day6-7: Testing and Debugging;
- Day8:  Documentation.

## ER Diagram
- **: <img src="Systems/ER Diagram.png" alt="ERDiagram">

## Algorithms

- **: ![Algorithm](Systems\Algorithm.png)
## Task Sheet

# Task Sheet: Online Food Ordering System

## Module 1: Customer

### 1.1 Registration Page

* Create a registration page for customers
* Require minimal information (name, email, password, contact number)
* Validate user input

### 1.2 Login Page

* Create a login page for registered customers
* Validate user credentials

### 1.3 Search Feature

* Implement a search feature to find hotels and dishes
* Allow filtering by food type (Main, Staters etc.)

### 1.4 Online Ordering

* Create a page for customers to select dishes and book orders
* Calculate total cost and display order summary

### 1.5 Change Password

* Create a page for customers to change their passwords

## Module 2: Restaurant Owner

### 2.1 Registration Page

* Create a registration page for restaurant owners
* Require minimal information (name, email, password, restaurant name)
* Validate user input

### 2.2 Login Page

* Create a login page for registered restaurant owners
* Validate user credentials

### 2.3 Dishes Management

* Create a page for restaurant owners to add/edit dishes
* Include fields for price, picture, and description

### 2.4 Upload Menu

* Create a page for restaurant owners to upload menu card pictures

### 2.5 Orders Management

* Create a page for restaurant owners to view orders
* Include filtering options (Pending, Delivered, etc.)

## Module 3: Admin

### 3.1 Dashboard

* Create a dashboard for admin to overview books, users, and categories

### 3.2 Categories Management

* Create a page for admin to add/delete categories

### 3.3 Food-Type Management

* Create a page for admin to add/delete food types (Main/Starters etc.)

### 3.4 Reporting

* Create a page for admin to generate reports on hotels and customers

## Functional Requirements

* Online menus (original and searchable format)
* Provision for restaurant owners to register with their menu
* Easy lookup of hotels in the area
* Check ratings and review hotels
* Simple, fast, and convenient food ordering
* Availability of menu online 24/7/365
* Accurate menu with pictures
* Prior knowledge of delivery time
* Base for online promotions and customer feedback

## Additional Tasks

* Design a user-friendly interface for the system
* Ensure security and data privacy for customers and restaurant owners
* Test and debug the system before deployment.

## Project Review and Monitoring Report

The project has been reviewed at various stages to ensure that it meets the requirements and follows best practices in
coding and file handling.

## Project Analysis

The project aimed to develop a Python-based online food ordering system, capable of managing various order operations. The development process comprised multiple stages, each presenting distinct challenges and opportunities for growth. The successful completion of the project showcases the effective implementation of Python programming concepts and online food ordering techniques, demonstrating a comprehensive understanding of both.

## Project Design

The project design includes:

- DFD (Data Flow Diagram)
:![DFD](Systems\DFD.png)
- Flowchart
 : ![Flowchart](Systems\Flowchart.png)
- Process Diagram
  : <img src="Systems/Process Diagram.png" alt="ProcessDiagram">
  that visually represent the project's workflow. These diagrams provide a clear understanding of the project's
structure and the interconnections between its various components.

## GUI Standard Doc
- GUI(Using Html,CSS & JS) 
<img src="Systems/GUI Standard.png" alt="GUI Doc">

## Interface Design Doc
- Interface Design
<img src="Systems/Interface Design.png" alt="Interface Design">

## Database Structure
- Database Structure/Design(Using Django) 
<img src="Systems/Db Structure.png" alt="DB Design">

## Screen Shots
Screenshots of the application's interface to illustrate its functionality:
![Screenshot (158).png](..%2F..%2F..%2F..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28158%29.png)
![Screenshot (155).png](..%2F..%2F..%2F..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28155%29.png)
![Screenshot (156).png](..%2F..%2F..%2F..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28156%29.png)
![Screenshot (157).png](..%2F..%2F..%2F..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20%28157%29.png)

## Source Codes with Comments
The source code of the project is provided below with detailed comments explaining each segment:

```Python
Home-Page -
{% extends 'main.html' %}
{% load static %}

{% block content %}
<main class="menu-layout">
  <div class="container">
    <h1 class="menu-title">Restaurant Menu</h1>

        <!-- Button Group for Meal Categories -->
    <div class="btn-group d-flex justify-content-center" role="group" aria-label="Meal Categories">
      <button class="btn btn-outline-primary" onclick="showAllMeals()">All</button>
        {% for meal in meals %}
          <button class="btn btn-outline-secondary" onclick="showMeals('{{ meal.0 }}')">{{ meal.1 }}</button>
        {% endfor %}
    </div>
    <!-- Meal Sections -->
    <div class="mt-3" id="menu">
      {% for meal in meals %}
        <div class="meal-section" data-meal-type="{{ meal.0 }}" style="display: none;">
          <div class="row row-cols-1 row-cols-md-3 g-4">
            {% for row in object_list %}
              {% if row.meal_type == meal.0 %}
                <div class="col">
                  <div class="card meal-card">
                    <img src="{{ row.image.url }}" class="card-img-top" alt="{{ row.meal }}">
                    <div class="card-body meal-card-body">
                      <h5 class="card-title"><a style="color: orange;" href="{% url 'menu_item_detail' row.pk %}">{{ row.meal }}</a></h5>
                      <p class="card-text">{{ row.description }}</p>
                    </div>
                    <div class="card-footer d-flex justify-content-between align-items-center">
                      <span class="badge bg-primary rounded-pill">{{ row.price }}$</span>
                      <a href="{% url 'add_to_cart' row.pk %}" class="btn btn-outline-success">Add to Cart</a>
                    </div>
                  </div>
                </div>
              {% endif %}
            {% endfor %}
          </div>
        </div>
      {% endfor %}
    </div>
      <p class="disclaimer">*Disclaimer: Want to leave a review? Kindly click on the order name.*</p>
  </div>
  <div class="mini-about">
    <div class="imgd">
      <img src="{% static 'images/3D_Sandwitch.png'%}" alt="" width="450">
    </div>
    <div class="about-text">
      <h3>We Are R-Foods</h3>
      <p>Welcome to R-foods, where we blend the warmth of traditional recipes <br> with a twist of modern culinary innovation. Our cozy restaurant is the perfect <br> spot for food lovers seeking to indulge in a diverse menu that pays homage to classic flavors <br> while embracing contemporary tastes. <br></p>
      <button class="btn-box">
        <a href="{% url 'about' %}" class="btn1">Explore</a>
      </button>
    </div>
  </div>
  <section id="reviews" class="body">
    <div class="reviews">
        <h3>What Says Our Customers From All Over </h3>
        <div class="reviews-img f-review" style="margin-top: 30px;">
            <img src="{% static 'images/client1.jpg'%}" alt="" width="150" style="border-radius: 50%; border: 2px solid #0000ff;">
            <h3>Elizabeth John</h3>
            <p>United Kingdom</p>
            <q>
              R-Foods never disappoints! The ambiance is cozy and inviting, perfect for a date night or a family dinner. I tried the grilled salmon with the chef’s special sauce, and it was divine. The flavors were balanced perfectly, and the presentation was top-notch. Can’t wait to come back and try more dishes! <br>
                Rating: ⭐⭐⭐⭐⭐
            </q>
        </div>
        <div class="reviews-img s-review" style="margin-top: 30px;">
            <img src="{% static 'images/client2.jpg'%}" alt="" width="150" style="border-radius: 50%; border: 2px solid #0000ff;">
            <h3>Steven Adebayo</h3>
            <p>Nigeria</p>
            <q>
              If you’re looking for a culinary adventure, R-Foods is the place to be. Their fusion cuisine is both innovative and delicious. I was particularly impressed with the spicy mango chicken & assorted jollof rice – it had just the right kick to it. The staff was friendly and attentive, making the whole dining experience delightful. <br>
              Rating: ⭐⭐⭐⭐⭐
            </q>
        </div>
        <div class="reviews-img t-review" style="margin-top: 30px;">
            <img src="{% static 'images/client3.jpg'%}" alt="" width="150" style="border-radius: 50%; border: 2px solid #0000ff;">
            <h3>Alia Chopra</h3>
            <p>India</p>
            <q>
              I visited R-Foods on a friend’s recommendation and it exceeded my expectations. The menu offers a great variety of options, catering to all tastes. I opted for the vegetarian lasagna, and it was the best I’ve ever had – rich, flavorful, and satisfying. The dessert menu is also worth exploring; the chocolate lava cake was heavenly!<br>
                Rating: ⭐⭐⭐⭐⭐
            </q>
        </div>
    </div>
</section>
</main>

<script>
  // Function to show all meals
  function showAllMeals() {
    var mealSections = document.getElementsByClassName("meal-section");
    for (var i = 0; i < mealSections.length; i++) {
      mealSections[i].style.display = "block";
    }
  }

  // Function to show specific meal category
  function showMeals(mealType) {
    var mealSections = document.getElementsByClassName("meal-section");
    for (var i = 0; i < mealSections.length; i++) {
      if (mealSections[i].getAttribute("data-meal-type") === mealType) {
        mealSections[i].style.display = "block";
      } else {
        mealSections[i].style.display = "none";
      }
    }
  }

  // Initially show all meals
  document.addEventListener("DOMContentLoaded", function() {
    showAllMeals();
  });
</script>
<style>
  .menu-title {
    text-align: center;
    color: orange;
    margin-top: 2rem;
}
.btn-group .btn {
    margin: 0.2rem;
}
.meal-card {
    border: none;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: transform 0.2s;
    margin-top:15px;
}
.meal-card:hover {
    transform: scale(1.05);
}
.meal-card img {
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    object-fit: cover;
    width: 100%;
    height: 200px;
}
.meal-card-body {
    padding: 1rem;
    background-color: #ffffff;
}
.badge {
    font-size: 1rem;
}
.card-footer {
    background-color: transparent;
    border-top: none;
}
.cart-link, .staff-links a {
    display: inline-block;
    margin: 0.5rem;
    text-decoration: none;
    color: #007bff;
}
.cart-link:hover, .staff-links a:hover {
    text-decoration: underline;
}
</style>
{% endblock %}

```

## User Guide
This section provides detailed instructions on how to use the Online Ordering System to perform various operations:
- **Customer**
- **Registration**
- Go to the registration page and fill in your details;
- Verify your email address and password;
- Log in to access the system.

- **Search and Order**
- Search for restaurants and dishes by name or location;
- Filter results by food type;
- Select dishes and create an order;
- View order summary and confirm.

- **Account Management**
- Change your password;
- Update your profile information.

- **Restaurant Owner**
- **Registration**
- Go to the registration page and fill in your details;
- Verify your email address and password;
- Log in to access the system.

- **Menu Management**
- Add and edit dishes with prices, pictures, and descriptions;
- Upload menu card pictures;
- Select food types.

- **Order Management**
- View and manage orders for the day;
- Filter orders by status (Pending, Delivered etc.).

- **Account Management**
- Change your password;
- Update your profile information.

- **Admin**
- **DashBoard**
- View overview of books, users, and categories;
- Manage categories and food types;
- Generate reports on hotels and customers.

- **Account Management**
- Change your password;
- Update your profile information;
- Recover your password.

## Developers Guide-Module Description
This section provides insights into the implementation details of the Online Ordering System, guiding developers on how to understand and extend its functionality:
- **Setup**
- Install the Django framework;
- Set up the database schema;
- Configure the system settings.

- **Modules**
- Customer: registration, login, search, order, account management;
- Restaurant Owner: registration, menu management, order management, account management;
- Admin: dashboard, category management, food type management, reporting, account management.
- **Functional Requirements**
- Online menus (original and searchable format);
- Restaurant owner registration with menu upload;
- Easy hotels lookup;
- Ratings and reviews;
- Simple ordering process;
- Menu availability online 24/7/365;
- Accurate menu with pictures;
- Delivery time estimation;
- Base for online promotions and customer feedback.
- **Technical Requirements**
- Django FrameWork;
- Database schema;
- System settings configuration;
- Security and data privacy measures.

## Final Check List
- [x] Code compiles without errors.
- [x] All functionalities have been implemented as per the problem statement.
- [x] Code has been reviewed and optimized.
- [x] Documentation is complete and accurate.

## Conclusion
The Online Food Ordering System offers a robust and user-friendly platform for restaurants and customers to interact and transact. As a user, you can effortlessly browse menus, place orders, and manage your account. As a developer, you can leverage the system's extensibility and modify it to suit your specific needs. This guide will walk you through the features and functionality of the Online Food Ordering System, built with Django, HTML, CSS, and JavaScript.

## *Developers Information*:
- **_Developed By_**: *Akinsulire Solomon Olabode, Adebayo Olamigoke David & Makanjuola Kafayat Adebunkola*.
- **_GitHub Repository_**: *https://github.com/Olamigoke10/OnlineStoreWithDjango.git*
- **_Start Date_**: 11th, June 2024.
- **_End Date_**: 23th, June 2024.
