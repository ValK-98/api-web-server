# T2A2 API Webserver Project
## Valentinas Kornijenka
[Github Repo](https://github.com/ValK-98/api-web-server)

### **R1 - Identification of the problem you are trying to solve by building this particular app.**

I am building an API app to serve as a smartwatch comparison tool. Currently it is difficult for users to get concise information on the plethora of available smartwatches on the market. For users to do research of smartwatches they would like to purchase they typically have to go through websites and Youtube videos which either have a lot of filler text or Youtube videos that sometimes can take a considerable amount to watch. This app would allow users to look up smartwatches and quickly see their pros & cons. 

### **R2 - Why is it a problem that needs solving?**

The smartwatch industry is fast growing and as with other fields of tech there are constant new updates and improvements with each new generation of smartwatches. As the smartwatch industry is relatively new, the typical consumer looking to purchase a smartwatch has an overwhelming amount of options to pick from. For example, Apple alone has 5 variants of current generation smartwatch while Garmin has 6 main models and a few other variants that they offer. This leads to an immense amount of research needed to make an informed purchase. Users have to consider factors such as looks, battery life, durability and how the product suits their lifestyle. Not to mention the different health features that smartwatches have to set them apart. All whilst figuring out which of the aforementioned features work the most consistently and reliably. Company websites don't tend to give a streamline and objective comparison of their models versus competitors but internet articles and Youtube videos can be quite lengthy with a lot of filler. By solving this issue we provide the user with a centralized, concise database that would save time and help them make an informed decision. 

### **R3 - Why have you chosen this database system. What are the drawbacks compared to others?**

I've chose to use PostgreSQL for this project as it's reliable and able to manage large amounts of data. Additionally, it's open-source, widely used and is fully ACID compliant. 

Part of the selection process was comparing it to other database systems, such as MongoDB. Here are the drawbacks of each:

### Drawbacks of PostgreSQL: 
* Performance can be slower than NoSQL databases when handling volumes of write-heavy transactions. 
* Lack of flexibility due to using a schema structure, which requires defining schemas in advance. As apps evolve this can cause issues since schemas may need to be updated as apps advance. 
* Limited built-in tools for certain tasks such as full-text search and handling geographic data. This can cause additional workload on processing as these tools are not natively available. 
* Whilst PostgreSQL has a large community support, in a commercial setting support may be more limited compared to more enterprise focused databases.


### Drawbacks of MongoDB: 
* MongoDB can use more memory & storage due to it storing data in BSON format. 
* Lack of rigidity can cause issues in data normalization. It additionally does not enforce foreign key constraints which can cause issues for data integrity.
* MongoDB has a document size limit which forces a careful design of databases. 
* There is potential for over-indexing which can lead to overheads in terms of storage and can impact write performance. 

The choice between MongoDB and PostgreSQL is highly situational. They are both strong choices for databases systems, however for different needs. If using complex queries and ensuring ACID compliance are important - PostgreSQL is the best choice. On the other hand, if fast write operations are needed as well as the handling of unstructured data then MongoDB may be preferable. As the latter will not be necessary for this project, PostgreSQL is a better choice. 

Sources:

https://kinsta.com/blog/mongodb-vs-postgresql/#mongodb-vs-postgresql-headtohead-comparison

https://aws.amazon.com/compare/the-difference-between-mongodb-and-postgresql

https://www.mongodb.com/compare/mongodb-postgresql



### **R4 - Identify and discuss the key functionalities and benefits of an ORM**

An Object-Relational Mapping (ORM) is a programming technique that is used to map incompatible data from a programming language into data that a relational database can use. 

**Some of it's key functionalities are:**

* Data Abstraction:
    * ORM abstract the database system, allowing developers to work with data as objects, reducing the need to write SQL queries. However, this can sometimes lead to inefficient queries if the ORM is not used carefully.

* Database Synchronization:
    * ORM synchronizes the database schema with the application model. Changes in the model can be automatically propagated to the database schema. In large projects however, this can lead to a need to have the database schema carefully managed to prevent mistakes or data loss.

* CRUD Operations:
    * Simplifies Create, Read, Update, and Delete (CRUD) operations. Developers interact with objects rather than SQL. Sometimes this can hide the complexity of the operations thus impacting the performance implications.

* Query Capability:
    * Provides a querying capability that lets developers write queries using the programming language's features rather than SQL. But sometimes this can be less effective than writing native SQL queries, especially for complex operations. 


**Some of it's key benefits are:**

* Increased Productivity:
    * Automates boilerplate code for database operations, allowing developers to focus on business logic. However this can lead to a potential lack of understanding of the underlying database operations. 

* Maintainability:
    * Code is more maintainable and understandable, as it aligns with the application's domain model. However the nuance is that complex queries can become more convoluted.

* Reduced SQL Injection Risk:
    * By abstracting SQL queries, ORMs can reduce the risk of SQL injection attacks. However, this does not eliminate the need for careful security practices. Especially if raw SQL is still used for complex queries. 

* Integration with Application Logic:
    * Seamless integration with the programming language's own constructs. But, this can sometimes lead to a blurring of boundaries between the database layer and application logic.


ORMs provide a convenient and efficient way to interact with databases, however their use requires an understanding of their limitations as well as the database system in use. 

### **R5 - Document all endpoints for your API**

### **R6 - An ERD for your app**

### **R7 - Detail any third party services that your app will use**

### **R8 - Describe your projects models in terms of the relationships they have with each other**

### **R9 - Discuss the database relations to be implemented in your application**

### **R10 - Describe the way tasks are allocated and tracked in your project**



