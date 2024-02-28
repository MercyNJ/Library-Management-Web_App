<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <h1>LibraWeb</h1>
  <img src="../static/images/libraryhome.jpg" alt="Home Image" class="image">
  <h2>Introduction</h2>
  <p>Welcome to Libra Web, a web application meticulously crafted to cater to the unique needs of a single library and its librarian. The primary goal of this project is to automate and streamline essential operational processes, including members and books management, book issuance, and the generation of statements for reminder purposes. Libra Web offers an efficient and user-friendly solution tailored specifically for this library, ensuring a seamless experience for the librarian in managing day-to-day operations.</p>
    
  <h2>Key Objectives</h2>
  <ul>
   <li>Enhance efficiency in daily operations.</li>
   <li>Reduce manual tasks and paperwork.</li>
   <li>Provide a user-friendly platform specifically designed for librarians.</li>
  </ul>

  <h2>Benefits</h2>
   <p>By using Libra Web, the librarian can expect:</p>
   <ul>
   <li>Time savings in daily operations.</li>
   <li>Improved accuracy in record-keeping.</li>
   <li>Streamlined processes for enhanced productivity.</li>
   </ul>

   <h2>Important Link</h2>
   <p><a href="#">Web App Demo</a></p>

   <h2>Features</h2>
   <p>The web app allows the librarian to perform 4 main functions in regards to streamlining operations:</p>
   <h3>Members Records Management:</h3>
   <p>This functionality enables the librarian effortless access, addition, and removal of library members, optimizing operational efficiency. The web app replaces manual record-keeping with a modern, efficient solution for a seamless user experience.</p>
   <img src="../static/images/viewmembers.png" alt="LibraWeb members">

   <h3>Books Record management:</h3>
   <p>Similar to the members management function, the web application provides a streamlined process for the librarian to view all the books available, add new books, and delete book records as needed</p>
   <img src="../static/images/viewbooks.png" alt="LibraWeb books">

   <h3>Issuance Creation:</h3>
   <p>Within the web app, the librarian can effortlessly issue books. The process involves selecting a member from a dropdown menu, specifying books and quantities & setting a due date A warning is triggered if the selected quantity exceeds the available book stock, ensuring precision in both book issuance and books stock management.</p>
   <img src="../static/images/newissuance.png" alt="LibraWeb issuance">

   <h3>Statements of Reminder Generation:</h3>
   <p>Utilizing the web app, the librarian can effortlessly access a compilation of all active issuances, encompassing issuances whose return status is either overdue or borrowed. Additionally, the librarian can filter for active issuances pertaining to a specific member by either their ID or name. With this information, generating a statement of reminder for the chosen member is a straightforward process—simply by clicking the "Generate Statement" button.</p>
   <img src="../static/images/newstatement.png" alt="LibraWeb statement">

   <h2>Usage:</h2>
   <p>As this web application is currently tailored for a specific library, its use requires authentication. Upon accessing the designated domain in the browser, the librarian is directed to the initial login page where they must authenticate with their credentials. Additionally, they have the capability to change their password during this login process.</p>
   <img src="../static/images/login.png" alt="LibraWeb login">

   <p>Once successfully logged in, they gain access to the home page, where a sidebar menu facilitates easy navigation to various sections of the web application. From the home page, the librarian can efficiently manage members and books records, create new entries, issue books and generate statements of reminder as needed. Furthermore, the option to download the issuance records or statements is readily available for their convenience.</p>
   <img src="../static/images/welcomehome.png" alt="LibraWeb welcome">

   <h2>Technical Challenges Overcome</h2>
   <h3>Handling many-to-many data models relationships</h3>
   <p>Faced with the intricate challenges of managing many-to-many relationships, I took it upon myself to dive deep into the inner workings of Libra Web's data architecture. Guided by insights from SQLAlchemy documentation, I forged ahead, introducing association tables to forge clear connections between books and issuances. This endeavor demanded extensive fine-tuning across the application, every adjustment made with precision. The result? A robust foundation laid for enhanced performance and user satisfaction, setting the stage for a seamless experience as I embarked on the development journey with the application.</p>

   <h3>User Authentication</h3>
   <p>Implementing user authentication with Flask Login posed challenges that I effectively addressed. Errors arose, including misconfigurations in user session setup and data retrieval issues. A meticulous review of the Flask Login documentation proved instrumental. Specific challenges encountered and resolved included fine-tuning user session management and addressing intricacies in data retrieval. This experience underscored the importance of detailed documentation exploration, enhancing my proficiency in seamlessly integrating Flask Login for secure user authentication.</p>

   <h2>Moving Forward</h2>
   <p>As of now, I've conducted tests for the console, the database storage file, and the models. Going forward, my focus will be on expanding the test coverage to include functionalities within each Flask folder. This will encompass various aspects such as members, books, issuances, and statements, ensuring comprehensive testing across all components of the application. I am also working on deploying the app on PythonAnywhere.</p>

   <h2>Contributing Guidelines:</h2>
   <p>I appreciate your interest in reviewing or contributing to LibraWeb. I value your suggestions for new features and improvements. If you have ideas for new features or improvements, please feel free to contact me.</p>

   <h2>Author:</h2>
   <p>Mercy Njuguna<br>
   Github - <a href="https://github.com/MercyNJ">https://github.com/MercyNJ</a><br>
   Email - mercinjuguna@gmail.com<br>
   LinkedIn - <a href="https://www.linkedin.com/in/mercy-njuguna/">https://www.linkedin.com/in/mercy-njuguna/</a></p>
</body>
</html>
