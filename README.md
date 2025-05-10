# AetherNet

## 🚀 Current Features

### ✅ Live Climate Simulation
- Generates **temperature, humidity, and rainfall** data dynamically.
- Adjusts values based on **seasonal variations and time of day**.

### ✅ Automated Decision-Making
- Uses **HVAC & rainwater logic** to optimize system operations:
  - **Stores rainwater** when humidity is high & it's raining.
  - **Redirects excess water** to irrigation if tank levels are full.
  - **Increases heating** when temperatures are low.

### ✅ User Override System
- Allows manual control over automation:
  - **"Force Rainwater Storage"** → Stores rainwater regardless of conditions.
  - **"Force Rainwater Redirection"** → Redirects water instead of storing.

### ✅ Web UI with Live Updates
- Displays **sensor data on a dashboard** (`/sensor-data`).
- Uses **real-time graphs (Chart.js)** to visualize climate trends.
- Provides **instant override feedback** for user interactions.

### Override buttons

Override buttons are useful because they give the user manual control over the system rather than relying only on automation.

- If automation makes a bad decision, users can manually adjust behavior.
`Example: If the system incorrectly redirects water when storage is needed, the user can override and store rainwater manually.`
- In case of unexpected conditions (e.g., rapid weather changes), users can respond faster than automation.
`Example: A sudden storm causes flooding, so the user overrides the system to redirect rainwater immediately.`
- Not every user wants strict automation—having overrides makes the system more user-friendly.
`Example: Some users prefer to store rainwater regardless of weather trends, while others prioritize irrigation needs.`

### 🔹 System Sequence Diagram (Message Flow)

![MQTT Image Flow](/assets/mgtt_flow.png)

- **Sensors publish environmental data via MQTT.**  
- **Flask receives and processes the data, applying automation rules.**  
- **Web Dashboard subscribes to MQTT topics for real-time visualization.**  

### Frontend
•
HTML (HyperText Markup Language): This is the backbone of any website, providing the basic structure and content. HTML elements define headings, paragraphs, links, images, and other essential components.

•
CSS (Cascading Style Sheets): CSS is used to style the HTML elements, controlling the layout, colors, fonts, and overall visual appearance of the website. It ensures that the website is aesthetically pleasing and consistent across different devices.

•
JavaScript: While websites are generally less interactive than web apps, JavaScript can still be used to add dynamic elements such as sliders, forms, and simple animations, enhancing the user experience.

### Back End(Server-Side):

•
Web Server: This is the hardware or software that serves the website’s content to users. Common web servers include Apache, Nginx, and Microsoft IIS. The web server handles requests from users’ browsers and delivers the appropriate HTML, CSS, and JavaScript files.

•
Database: Websites often use databases to store and manage content. Databases like MySQL, PostgreSQL, or MongoDB can be used to store articles, images, user data, and other content that needs to be dynamically retrieved and displayed on the website.

•
Server-Side Processing: Languages like PHP, Python, Ruby, Java, C#, or Node.js are used to create dynamic content and interact with the database. For example, a PHP script might retrieve the latest blog posts from a database and format them into HTML to be displayed on the website

### Types of APIs

•
REST (Representational State Transfer): RESTful APIs use HTTP requests to perform CRUD (Create, Read, Update, Delete) operations. They are stateless and rely on standard HTTP methods like GET, POST, PUT, and DELETE.

•
SOAP (Simple Object Access Protocol): SOAP APIs use XML-based messaging protocols and are known for their robustness and security features. They are often used in enterprise-level applications.

•
GraphQL: A query language for APIs that allows clients to request specific data, reducing the amount of data transferred over the network. It provides more flexibility compared to REST.

### Key Concepts

•
Endpoints: Specific URLs where API services are accessed. Each endpoint corresponds to a particular function or resource.

•
Authentication and Authorisation: Ensuring that only authorised users can access certain API endpoints. Common methods include API keys, OAuth, and JWT (JSON Web Tokens).

•
Rate Limiting: Controlling the number of API requests a user can make within a certain time frame to prevent abuse and ensure fair usage.

### Design Principles to bare in mind learn from the course:

- Follow best practices such as using consistent naming conventions, versioning your API, and providing clear documentation.

### Security Considerations

•
Data Encryption: Use HTTPS to encrypt data transmitted between the client and the server.

•
Input Validation: Validate and sanitise inputs to prevent security vulnerabilities like SQL injection and cross-site scripting (XSS).

•
Access Control: Implement role-based access control (RBAC) to restrict access to sensitive endpoints.

### Best Practices:
•
Documentation: Provide comprehensive and clear documentation for your API, including usage examples, error codes, and response formats.

•
Testing: Use tools like Postman or automated testing frameworks to thoroughly test your API endpoints.

•
Monitoring and Analytics: Implement monitoring tools to track API usage, performance, and errors.

### Create a Login 

### Scalability:

Scalability ensures that a web app can handle increased loads without compromising performance. Techniques such as load balancing, caching, and using microservices architecture are essential for achieving scalability.

Security is paramount in web application development to protect sensitive data and ensure user trust. Practices include data encryption (using HTTPS), input validation to prevent vulnerabilities like SQL injection and cross-site scripting (XSS), and implementing authentication and authorisation mechanisms.

Regular security audits and keeping software up to date are also crucial for maintaining security.