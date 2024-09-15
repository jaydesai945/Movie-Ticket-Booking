import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import pymysql

class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Movie Ticket Booking System")
        self.root.geometry("850x350")
        self.root.configure(background='#f0f0f0')
        
        ttk.Label(self.root, text="Welcome to Movie Ticket Booking System", font=("Arial", 32), background='#f0f0f0').pack(pady=20)
        ttk.Label(self.root, text="Book your favorite movies tickets", font=("Roboto", 14), background='#f0f0f0').pack(pady=10)
        ttk.Button(self.root, text="see movies", command=self.open_movie_booking_app).pack(pady=10)
        ttk.Button(self.root, text="see booking details", command=self.see_booking_details).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.exit).pack(pady=10)
    def see_booking_details(self):
        booking_id = self.prompt_booking_id()
        if booking_id:
            self.display_booking_details(booking_id)
            
    def prompt_booking_id(self):
        booking_id_window = tk.Toplevel(self.root)
        booking_id_window.title("Enter Booking ID")
        booking_id_window.geometry("300x100")
        ttk.Label(booking_id_window, text="Enter Booking ID:").pack(pady=5)
        booking_id_entry = ttk.Entry(booking_id_window)
        booking_id_entry.pack(pady=5)
        
        def get_booking_id():
            booking_id = booking_id_entry.get().strip()
            booking_id_window.destroy()
            self.display_booking_details(booking_id)

        submit_button = ttk.Button(booking_id_window, text="Submit", command=get_booking_id)
        submit_button.pack(pady=2)

        booking_id_entry.focus_set()
        booking_id_entry.bind("<Return>", lambda event: get_booking_id())

    def display_booking_details(self, booking_id):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Mahars09@',
                database='project_db'       
            )
            c = conn.cursor()
            c.execute("SELECT * FROM bookings WHERE booking_id = %s", (booking_id,))
            booking_data = c.fetchone()
            conn.close()
    
            if booking_data:
                details_window = tk.Toplevel(self.root)
                details_window.title("Booking Details")
                details_window.geometry("300x30")
    
                labels = ["Booking ID", "Movie Title", "Date", "Time Slot", "Number of Seats", "Customer Name", "Mobile Number", "Payment Method", "Payment Cost"]
                for i, label_text in enumerate(labels):
                    tk.Label(details_window, text=label_text, anchor="w", padx=10).grid(row=i, column=0, sticky="w")
                    tk.Label(details_window, text=booking_data[i], anchor="w", padx=10).grid(row=i, column=1, sticky="w")
    
            else:
                messagebox.showerror("Error", "Please Enter Valid Booking id.")
        except Exception as e:
            print("Error:", e)
    def open_movie_booking_app(self):
        root = tk.Tk()
        app = MovieTicketBookingApp(root)
        root.mainloop()

    def exit(self):
        self.root.destroy()  # Close the welcome page

class MovieTicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.movie_selection_frame = ttk.Frame(self.root)
        self.movie_selection_frame.pack(pady=20)
        self.populate_movies()

    def book_tickets(self, movie_details):
       title, duration, rating, genre, price, starcast = movie_details
       try:
           conn = pymysql.connect(
               host='localhost',
               user='root',
               password='Mahars09@',
               database='project_db'
           )
           c = conn.cursor()
           c.execute("SELECT time_slot1_seats, time_slot2_seats, time_slot3_seats FROM movies WHERE title = %s", (title,))
           time_slots_seats = c.fetchone()
           available_seats = sum(time_slots_seats)
           conn.close()
   
           # Create a new window for displaying detailed movie information
           details_window = tk.Toplevel(self.root)
           details_window.title(f"Movie Details: {title}")
           details_window.geometry("600x300")
   
           # Display movie details
           ttk.Label(details_window, text=f"Title: {title}", font=("Arial", 14)).pack(pady=5)
           ttk.Label(details_window, text=f"Duration: {duration} mins").pack(pady=5)
           ttk.Label(details_window, text=f"Rating: {rating}").pack(pady=5)
           ttk.Label(details_window, text=f"Genre: {genre}").pack(pady=5)
           ttk.Label(details_window, text=f"Price: {price}").pack(pady=5)
           ttk.Label(details_window, text=f"Star Cast: {starcast}").pack(pady=5)
   
           # Display available seats and book now button
           ttk.Button(details_window, text="Book Now", command=lambda: self.display_time_options(title, time_slots_seats)).pack(pady=5)
   
       except Exception as e:
           print("Error:", e)

    def display_time_options(self, title, time_slots_seats):
          date_options = ["2024-04-06", "2024-04-07", "2024-04-08", "2024-04-09", "2024-04-10"]  # Sample dates
          date_window = tk.Toplevel(self.root)
          date_window.title(f"Select Date for {title}")
          date_window.geometry("400x300")
      
          ttk.Label(date_window, text=f"Movie: {title}", font=("Arial", 12, "bold")).pack(pady=5)

          def select_date(date):
              date_window.destroy()
              time_options = ["9:00 AM", "1:00 PM", "5:00 PM"]
              time_window = tk.Toplevel(self.root)
              time_window.title(f"Select Time for {title} on {date}")
              time_window.geometry("400x200")  
      
              ttk.Label(time_window, text=f"Movie: {title}").pack(pady=5)
              ttk.Label(time_window, text=f"Date: {date}").pack(pady=5)
  
              for time_slot in time_options:
                  def book_now(slot=time_slot, seats=time_slots_seats[time_options.index(time_slot)]):
                      book_window = tk.Toplevel(time_window)
                      book_window.title(f"Booking: {slot} on {date}")
                      book_window.geometry("400x400")
      
                      ttk.Label(book_window, text=f"Selected Time: {slot}").pack(pady=5)
                      ttk.Label(book_window, text=f"Available Seats: {seats}").pack(pady=5)
      
                      ttk.Label(book_window, text="Name:").pack(pady=2)
                      name_entry = ttk.Entry(book_window)
                      name_entry.pack(pady=2)
      
                      ttk.Label(book_window, text="Mobile Number:").pack(pady=2)
                      mobile_entry = ttk.Entry(book_window)
                      mobile_entry.pack(pady=2)
      
                      ttk.Label(book_window, text="Number of Seats:").pack(pady=2)
                      seats_entry = ttk.Entry(book_window)
                      seats_entry.pack(pady=2)
      
                      payment_methods = ["Credit Card", "Debit Card","Google pay","Paytm"]
                      ttk.Label(book_window, text="Payment Method:").pack(pady=2)
                      payment_var = tk.StringVar(book_window)
                      payment_var.set(payment_methods[0])
                      payment_dropdown = ttk.Combobox(book_window, textvariable=payment_var, values=payment_methods,state="readonly")
                      payment_dropdown.pack(pady=2)
      
                      confirm_button = ttk.Button(book_window, text="Confirm Booking", command=lambda: self.confirm_booking(title, date, slot, seats, name_entry.get(), mobile_entry.get(), seats_entry.get(), payment_var.get(),book_window))
                      confirm_button.pack(pady=5)
      
                  ttk.Button(time_window, text=f"Book for {time_slot}", command=book_now).pack(pady=5)
      
          for date in date_options:
              ttk.Button(date_window, text=date, command=lambda date=date: select_date(date)).pack(pady=5)

    def confirm_booking(self, title, date, time_slot, available_seats, name, mobile, num_seats, payment_method, book_window):
       try:
           conn = pymysql.connect(
               host='localhost',
               user='root',
               password='Mahars09@',
               database='project_db'
           )
           c = conn.cursor()
       
           # Calculate payment cost
           if not num_seats :
               messagebox.showerror("Error", "Please enter a valid no of seats.")
               return
           c.execute("SELECT price FROM movies WHERE title = %s", (title,))
           price = c.fetchone()[0]
           payment_cost = int(num_seats) * price
           if not name:
               messagebox.showerror("Error", "Please enter a name.")
               return
           if not mobile.isdigit() or len(mobile)!=10 :
               messagebox.showerror("Error", "Please enter a valid mobile number.")
               return
           if not mobile.isdigit() or len(mobile)!=10 :
               messagebox.showerror("Error", "Please enter a valid mobile number.")
               return
           mobile = int(mobile)
           # Validate the number of seats
           if not num_seats.isdigit() or int(num_seats) <= 0 or int(num_seats) > 10:
               messagebox.showerror("Error", "Please enter a valid number of seats (1 to 10).")
               return
       
           # Check if there are enough available seats for the selected time slot
           if int(num_seats) > available_seats:
               messagebox.showerror("Error", "Sorry, there are not enough available seats for the selected time.")
               return
       
           # Determine which time slot was selected and update the corresponding seats
           if time_slot == "9:00 AM":
               c.execute("UPDATE movies SET time_slot1_seats = %s WHERE title = %s", (available_seats - int(num_seats), title))
           elif time_slot == "1:00 PM":
               c.execute("UPDATE movies SET time_slot2_seats = %s WHERE title = %s", (available_seats - int(num_seats), title))
           elif time_slot == "5:00 PM":
               c.execute("UPDATE movies SET time_slot3_seats = %s WHERE title = %s", (available_seats - int(num_seats), title))
       
           # Insert booking data into the database
           c.execute("INSERT INTO bookings (movie_title, date, time_slot, number_of_seats, customer_name, mobile_number, payment_mode, payment_cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                     (title, date, time_slot, num_seats, name, mobile, payment_method, payment_cost))
           conn.commit()
           
           c.execute("SELECT LAST_INSERT_ID()")
           booking_id = c.fetchone()[0]
           
           conn.close()
       
           # Close the book window after confirming booking
           book_window.destroy()
       
           # Display a message confirming the booking
           messagebox.showinfo("Booking Confirmed", "Your booking has been confirmed.")
       
           # Display details of the booking
           self.confirm_booking_details(booking_id,title, date, time_slot, num_seats, name, mobile, payment_method, payment_cost)
       
       except Exception as e:
           print("Error:", e)

           

    def confirm_booking_details(self,booking_id,title, date, time_slot, num_seats, name, mobile, payment_method, payment_cost):
           details_window = tk.Toplevel(self.root)
           details_window.title("Booking Details")
           details_window.geometry("400x400")
       
           ttk.Label(details_window, text="Booking Details", font=("Arial", 16, "bold")).pack(pady=10)
       
           ttk.Label(details_window, text=f"Booking ID: {booking_id}").pack(pady=5)
           ttk.Label(details_window, text=f"Movie Title: {title}").pack(pady=5)
           ttk.Label(details_window, text=f"Date: {date}").pack(pady=5)
           ttk.Label(details_window, text=f"Time Slot: {time_slot}").pack(pady=5)
           ttk.Label(details_window, text=f"Number of Seats: {num_seats}").pack(pady=5)
           ttk.Label(details_window, text=f"Customer Name: {name}").pack(pady=5)
           ttk.Label(details_window, text=f"Mobile Number: {mobile}").pack(pady=5)
           ttk.Label(details_window, text=f"Payment Method: {payment_method}").pack(pady=5)
           ttk.Label(details_window, text=f"Payment Cost: {payment_cost}").pack(pady=5)




    def populate_movies(self):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='Mahars09@',
                database='project_db'
            )
            c = conn.cursor()
            c.execute("SELECT title, duration, rating, genre, price, starcast FROM movies")
            movies_data = c.fetchall()

            # Configure padding for all frames
            pad_x = 10
            pad_y = 5

            # Create a counter for grid placement
            row_counter = 0
            column_counter = 0            
            for movie in movies_data:
                title, duration, rating, genre, price, starcast = movie

                # Create a frame for each movie
                movie_frame = ttk.Frame(self.movie_selection_frame, relief="groove", borderwidth=2)
                movie_frame.grid(row=row_counter, column=column_counter, padx=pad_x, pady=pad_y, sticky="nsew")

                # Display movie details in the frame
                ttk.Label(movie_frame, text=f"Title: {title}", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, pady=2, sticky="w")
                ttk.Label(movie_frame, text=f"Duration: {duration} mins").grid(row=1, column=0, padx=5, pady=2, sticky="w")
                ttk.Label(movie_frame, text=f"Rating: {rating}").grid(row=2, column=0, padx=5, pady=2, sticky="w")
                ttk.Label(movie_frame, text=f"Genre: {genre}").grid(row=3, column=0, padx=5, pady=2, sticky="w")

                # Book Tickets Button
                book_tickets_btn = ttk.Button(movie_frame, text="Book Tickets", command=lambda movie_details=movie: self.book_tickets(movie_details))
                book_tickets_btn.grid(row=5, column=0, padx=5, pady=2, sticky="w")

                # Increment row_counter and column_counter
                row_counter += 1
                if row_counter > 2:  # Display 3 movies per row
                    row_counter = 0
                    column_counter += 1

            conn.close()
        except Exception as e:
            print("Error:", e)

def main():
    root = tk.Tk()
    welcome_page = WelcomePage(root)
    root.mainloop()

if __name__ == "__main__":  
    main()

