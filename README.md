## Diary App

### Description:
   Project uses Python and Tkinter for the user interface. It also uses the cryptography.fernet library to create a secret key.
   After the secret key is generated, and loaded, and a password is created which is stored in the .env file, authentication
   function authenticates the password, and then access is granted to the user.
   The user interface appears, that has a title, a dropdown Options Menu, three frames i.e. add_frame, view_frame, edit_frame
   that are enclosed in the enclosing_frame, and a result_frame.
   The title is placed on the label_frame. The add_frame is for adding an entry, and consists of labels for date, title and 
   content, and corresponding entry boxes. The view frame consists of a view_label and view_text_area that is a Scrolled text
   area for viewing the .txt files in the entries folder. The right frame consists of labels for reading an entry i.e. read_label
   and corresponding entry box i.e. read_name, search_label and search_entry entry box, delete_label and delete_entry entry box.
   At the bottom of the right_frame is a edit_label and edit_text_area. At the bottom of the enclosing_frame is the 
   result_text_area with its label i.e. the result_label. 
   Entering the complete .txt filename as appears in the view frame in read_name entry box, and clicking the Read option in 
   the Options Menu will display the decrypted contents of the file in the result_text_area.
   Entering a keyword in the search_entry box, and clicking the Search option in the Options Menu will display contents of that file
   in the result_text_area. The keyword should be a word in the file's title. Likewise, if a keyword is entered in the delete_entry 
   box, and Delete option is chosen from the Options Menu,  a file is selected, and deleted. The file selected for deletion has the 
   keyword in its title. A message that the file has been deleted, appears in the result_text_area.
   Finally, if the Edit option is chosen from the Options Menu, a popup will appear, and keyword has to be entered. Upon clicking OK,
   the decrypted text of the file appears in the edit_text_area. The user can modify the contents in the edit_text-area. The statement
   edit_text_area.after(30000, save_entry) calls the save_entry function after 30000 ms. The modified text from the edit_text_area
   is copied into the result_text_area. The file's modified contents are encrypted and saved to the file with the original name in the
   entries folder. Selecting the View option in the Options Menu, displays the current contents of the entries folder. The Clear View
   option when selected, clears the view_text_area. The Clear option when selected, clears all the entry boxes, and text areas in the
   user interface. Selecting the Exit option in the Options Menu enables exiting the program.

   ### How To Use
   Use conda to activate environment in which the project exists. Navigate to the project directory, and type python app.py. When the
   user interface appears, use the add frame to make an entry. Fill in the date, title and contents. Selecting the Add option will save 
   the encrypted version of the content to the folder entries as a .txt file. User can view the files in the entries folder by selecting 
   View from the View option of the Options Menu. To read  the contents of a particular file, full name of .txt file as appears in the
   View text area must be entered in the Read entry. The Read option should be selected from the Options Menu, and decrypted file contents
   appear in the result text area. For search and delete options, a keyword has to be entered in the respective entry boxes. The keyword
   must exist in the title of the file. Then the desired option should be chosen from the Options Menu. Upon clicking the appropriate
   option, the result will appear in the result text area. For the Edit option, clicking the Edit option in the Options Menu will display
   a popup. Keyword must be entered in the popup. Again, keyword should exist in the title of the file. Clicking OK will display the 
   decrypted contents in the result text area after a pause.

   ### Attribution:
   Image:
   <a href="http://www.freepik.com">Designed by rawpixel.com / Freepik</a>
   
   
