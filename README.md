# Simple Todo application API With DRF

<h3>This API include routes for Todo CRAD operations and User registration, loging-in and logout using token authentication.</h3>

<b>User API endpoints:</b>
<ul>
  <li>LOGIN        - POST:   {URL}/api-v1/account/login/</li>
  <li>REGISTER     - POST:   {URL}/api-v1/account/register/</li>
  <li>LOGOUT       - POST:   {URL}/api-v1/account/logout/</li>
</ul>

<b>Todos API endpoints:</b>
<ul>
  <li>CREATE TODO  - POST:   {URL}/api-v1/todos/</li>
  <li>UPDATE TODO  - PUT:    {URL}/api-v1/todos/PK/</li>
  <li>PATCH TODO   - PATCH:  {URL}/api-v1/todos/PK/</li>
  <li>TODO LIST    - GET:    {URL}/api-v1/todos/</li>
  <li>GET TODO     - GET:    {URL}/api-v1/todos/PK/</li>
  <li>DELETE TODO  - DELETE: {URL}/api-v1/todos/PK/</li>
</ul>
<b>*  PK is a ID of the todo.</b>
<br>
<b>** Note that all todo endpoints work only for authenticated user.</b>
