import flask
from flask import Flask, redirect,url_for, render_template,request
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session 
import os
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId
import time
import datetime

mydb = os.environ['db']
app = Flask(__name__, template_folder="templates")
client = pymongo.MongoClient(mydb)
db = client["ourdream"]
users_collection = db["db"]
app.secret_key = 'secret'
tasks_collection = db['tasks']
user_task_collection = db['user_task']
user_withdraw = db['withdraw']
user_deposit = db['deposit']


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phonenumber = request.form.get('phonenumber')  # Define the phonenumber variable here
        existing_user = users_collection.find_one({'phonenumber': phonenumber})

        if existing_user is None:
            hash_password = generate_password_hash(request.form.get('password'))

            # Set default values for account balance and task
            users_collection.insert_one({
                'phonenumber': phonenumber, 
                'password': hash_password,
                'account_balance': 0,  # Setting the default value for account balance
                'task': 0,  # Setting the default value for task
                'dailytask': 0
            })

            session['phonenumber'] = phonenumber
            return redirect(url_for('dashboard'))

        return 'User already exists'

    return render_template('register.html')  # This line handles the GET request, rendering the registration form.


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phonenumber = request.form.get('phonenumber')
        login_user = users_collection.find_one({'phonenumber': phonenumber})
        session['phonenumber'] = phonenumber

        if login_user and check_password_hash(login_user['password'], request.form.get('password')):
          return redirect(url_for('dashboard'))

    return render_template('login.html')  # Render the login form


@app.route('/dashboard')
def dashboard():
    if 'phonenumber' in session:
        user_data = users_collection.find_one({'phonenumber': session['phonenumber']})
        if user_data:
            phonenumber = user_data['phonenumber']
            account_balance = user_data['account_balance']  # Retrieve account balance from user data
            task = user_data['task']  # Retrieve task from user data
            dailytask = user_data['dailytask']  # Retrieve task from user data
            return render_template('dashboard.html', phonenumber=phonenumber, account_balance=account_balance, task=task,dailytask=dailytask)  # Pass account balance and task to the dashboard template
        else:
            return redirect(url_for('login'))  
    else:
        return redirect(url_for('login'))


   
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# plans

@app.route('/plan1')
def plan1():
  price = 2500
  total_videos = 3
  video1= 30
  plan_validity = 60
  url = "https://our-dream.notrana.repl.co/plan1/buy"

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity,url=url)
  
@app.route('/plan2')
def plan2():
  price = 5000
  total_videos = 6
  video1= 35
  plan_validity = 65

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan3')
def plan3():
  price = 8000
  total_videos = 8
  video1= 40
  plan_validity = 70

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan4')
def plan4():
  price = 12000
  total_videos = 10
  video1= 50
  plan_validity = 75

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan5')
def plan5():
  price = 15000
  total_videos = 11
  video1= 52
  plan_validity = 80

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan6')
def plan6():
  price = 20000
  total_videos = 15
  video1= 50
  plan_validity = 85

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan7')
def plan7():
  price = 25000
  total_videos = 17
  video1= 55
  plan_validity = 90

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan8')
def plan8():
  price = 30000
  total_videos = 19
  video1= 60
  plan_validity = 95

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan9')
def plan9():
  price = 40000
  total_videos = 22
  video1= 70
  plan_validity = 100

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan10')
def plan10():
  price = 55000
  total_videos = 25
  video1= 80
  plan_validity = 120

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)
@app.route('/plan11')
def plan11():
  price = 150000
  total_videos = 30
  video1= 230
  plan_validity = 365

  return render_template('plans.html', price=price, total_videos=total_videos, video1=video1, plan_validity=plan_validity)

# plan buy

# ... (previous code remains the same)

@app.route('/buy_plan/<int:plan_number>', methods=['POST','GET'])
def buy_plan(plan_number):
    # Define the prices and total videos for each plan
    plans = {
        1: {'price': 2500, 'total_videos': 3, 'days': 12},
        2: {'price': 5000, 'total_videos': 6, 'days': 24},
        3: {'price': 8000, 'total_videos': 8, 'days': 50},
        4: {'price': 12000, 'total_videos': 10, 'days': 65},
        5: {'price': 15000, 'total_videos': 11, 'days': 70},
        6: {'price': 20000, 'total_videos': 15, 'days': 75},
        7: {'price': 25000, 'total_videos': 17, 'days': 80},
        8: {'price': 30000, 'total_videos': 19, 'days': 85},
        9: {'price': 40000, 'total_videos': 22, 'days': 90},
        10: {'price': 55000, 'total_videos': 25, 'days': 95},
        11: {'price': 150000, 'total_videos': 30, 'days': 365},
        # Define other plan details here
    }
    subscription_start = datetime.datetime.now()
    subscription_end = subscription_start + datetime.timedelta(days=plan['days'])


    plan = plans.get(plan_number)

    if not plan:
        return "Invalid plan number"

    if 'phonenumber' in session:
        user_data = users_collection.find_one({'phonenumber': session['phonenumber']})
        if user_data:
            if user_data['account_balance'] >= plan['price']:  
                new_balance = user_data['account_balance'] - plan['price']

                # Check if the user already has a subscribed plan
                if 'subscribed_plan' in user_data:
                    current_plan_number = int(user_data['subscribed_plan'].replace('plan', ''))
                    current_plan = plans.get(current_plan_number)
                    total_videos = current_plan['total_videos'] + plan['total_videos']
                else:
                    total_videos = plan['total_videos']

                users_collection.update_one({'phonenumber': session['phonenumber']}, {'$set': {'task': total_videos}})
                users_collection.update_one({'phonenumber': session['phonenumber']}, {'$set': {'account_balance': new_balance}})
                users_collection.update_one({'phonenumber': session['phonenumber']}, {'$set': {'subscribed_plan': f'plan{plan_number}'}})
                users_collection.update_one({'phonenumber': session['phonenumber']}, {'$set': {'dailytask': total_videos}})
                users_collection.update_one({'phonenumber': session['phonenumber']}, {'$set': {'subscription_start': subscription_start}})
                users_collection.update_one({'phonenumber': session['phonenumber']}, {'$set': {'subscription_end': subscription_end}})
                return "Plan subscribed successfully!"
            else:
                return "Insufficient balance to buy the plan"
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

def is_subscription_expired(subscription_end_date):
  return datetime.datetime.now() > subscription_end_date


@app.route('/add_task')
def add_task():
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 1
       # Setting the default value for task
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 2
       # Setting the default value for task
  })

  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 3
       # Setting the default value for task
  })

  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 4
       # Setting the default value for task
  })

  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 5
       # Setting the default value for task
  })

  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 6
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 7
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 8
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 9
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 10
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 11
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 12
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 13
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 14
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 14
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 15
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 16
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 17
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 18
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 19
  })
  tasks_collection.insert_one({
      'video_url': 'https://www.youtube.com/watch?v=85fYnF5Jt-k', 
      'taskno': 20
  })
  return 'added'
  
@app.route('/tasks', methods=['GET'])
def display_tasks():
    tasks = tasks_collection.find()  # Fetch tasks from the database
    return render_template('tasks.html', tasks=tasks)

# @app.route('/task/<int:tasknumber>', methods=['GET'])
# def taskdoing(tasknumber):
#     task = tasks_collection.find_one({'taskno': tasknumber})
#     return render_template('task_intrection.html', task=task)
app.config['UPLOAD_FOLDER'] = "static/Uploads"

@app.route('/task/<int:tasknumber>', methods=['GET', 'POST'])
def task_interact(tasknumber):
    task = tasks_collection.find_one({'taskno': tasknumber})
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Save image path in the database
                #image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # user_task_collection.update_one({'taskno': tasknumber}, {'$set': {'image_path': image_path}})   
                user_task_collection.insert_one({"image_path": filename,"phonenumber": session['phonenumber'],"taskno": tasknumber, "status":"panding"})
                users_collection.find_one({'phonenumber': session['phonenumber']})
                total_video = task['taskno']
                current_user = users_collection.find_one({'phonenumber': session['phonenumber']})
                if current_user and current_user.get('dailytask', 0) > 0:
                    # Decrease dailytask by 1 if it's greater than 0
                    users_collection.update_one({'phonenumber': session['phonenumber']}, {'$inc': {'dailytask': -1}})
                else:
                  # Increase dailytask by 1 if it's less than 0
                    return "your task limit reached"

    return render_template('task_intrection.html', task=task)
#scheduler = BackgroundScheduler()
#scheduler.start()

def update_daily_task():
  users = users_collection.find()  # Fetch all users
  for user in users:
      task = user.get('task', 0)  # Get the 'task' value for the user
      users_collection.update_one(
          {'_id': user['_id']},
          {'$set': {'dailytask': task}}  # Update 'dailytask' to 'task'
      )


@app.route('/updatetask')
def update():
  update_daily_task()
  return "updated"
  time.sleep(2)
  return redirect("url_for('admin')")
#scheduler.add_job(update_daily_task, 'interval', hours=24)

#amount = request.form.get("amount")


@app.route("/withdraw", methods=["POST", "GET"])
def withdraw():
    if "phonenumber" in session:
      user = users_collection.find_one({'phonenumber': session['phonenumber']})
      account_balance = user.get("account_balance")  # Retrieve the account balance
      print(f"Account Balance: {account_balance}")
      if account_balance is not None and int(account_balance) >= 600:
        userphone = session["phonenumber"]
        wallet_no = request.form.get("walletno")
        wallettype = request.form.get("select_wallet")
        amount = request.form.get("amount")
          
          
        user_withdraw.insert_one({
                    "userphone": userphone,
                    "walletno": wallet_no,
                    "amount": amount,
                    "status": "panding",
                    "wallettype": wallettype
                })
        if amount is not None:
            users_collection.update_one({'phonenumber': session['phonenumber']}, {'$inc': {'account_balance': -int(amount)}})
        
        return render_template("withdraw.html")
          
      else:
          return "insufficient balance to withdraw"
          
           

@app.route("/deposite")
def deposite():
  if "phonenumber" in session:
    return render_template("deposit.html")
  else:
    return redirect("url_for('login')")

app.config['SS_FOLDER'] = "static/SSFOLDER"
@app.route("/deposite_jazzcash", methods=["POST", "GET"])
def deposite_jazzcash():
  if 'phonenumber' in session:
    if request.method == 'POST':
      if 'image' in request.files:
          image = request.files['image']

          if image.filename != '':
              filename = secure_filename(image.filename)
              image.save(os.path.join(app.config['SS_FOLDER'], filename))

              # Save image path in the database
              #image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
              amount = request.form.get("amount")
              walletno = request.form.get("walletno")
              transectionid = request.form.get("transectionid")
              user_deposit.insert_one({"image_path": filename,"userphonenumber": session['phonenumber'], "walletno": walletno, "transectionid": transectionid,"wallettype":"jazzcash","amount": amount,"status":"panding"})

    return render_template("deposite_jazzcash.html")

  else:
    return redirect("url_for('login')")



@app.route("/deposite_easypasa", methods=["POST", "GET"])
def deposite_easypasa():
  if 'phonenumber' in session:
    if request.method == 'POST':
      if 'image' in request.files:
          image = request.files['image']
          
          if image.filename != '':
              filename = secure_filename(image.filename)
              image.save(os.path.join(app.config['SS_FOLDER'], filename))

              # Save image path in the database
              #image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
              amount = request.form.get("amount")
              walletno = request.form.get("walletno")
              transectionid = request.form.get("transectionid")
              user_deposit.insert_one({"image_path": filename,"userphonenumber": session['phonenumber'], "walletno": walletno, "transectionid": transectionid, "wallettype": "easypasa","amount":amount, "status":"panding"})
    
    return render_template("deposit_easypasa.html")

  else:
    return redirect("url_for('login')")
  
@app.route("/uecnkqjddklaskdjiiie")
def admin():
  
  return render_template("admin.html")


@app.route('/edit_task')
def edit_task():
    tasks = tasks_collection.find().sort([('taskno', 1)])  # Fetch all tasks ordered by task number
    return render_template('edit_tasks.html', tasks=tasks)



@app.route('/update_task', methods=['POST'])
def update_task():
    if request.method == 'POST':
        for task in tasks_collection.find().sort([('taskno', 1)]):
            task_no = str(task['taskno'])
            new_url = request.form.get(f'task{task_no}')
            tasks_collection.update_one({'taskno': task['taskno']}, {'$set': {'video_url': new_url}})
        return redirect(url_for('edit_task'))  # Redirect back to the edit_task page


@app.route('/task_review', methods=['GET'])
def task_review():
    pending_tasks = user_task_collection.find({'status': 'panding'})  # Fetch tasks with status 'panding'
    return render_template('task_review.html', tasks=pending_tasks)


@app.route('/update_task_status/<task_id>', methods=['POST'])
def update_task_status(task_id):
    # Fetch the task from the database using the task ID
    task = user_task_collection.find_one({'_id': ObjectId(task_id)})

    if task:
        # Update status to 'Done'
        user_task_collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'status': 'Done'}})

        # Increment the user's balance by 30
        user_phone = task.get('phonenumber')
        if user_phone:
            users_collection.update_one({'phonenumber': user_phone}, {'$inc': {'account_balance': 30}})

        return "Task status updated and balance added successfully!"

    return "Task not found"



@app.route('/withdraw_requests')
def withdraw_requests():
    pending_requests = user_withdraw.find({'status': 'panding'})
    return render_template('withdraw_req.html', requests=pending_requests)

@app.route('/update_status/<request_id>', methods=['POST'])
def update_status(request_id):
    # Update the status to 'Done' for the specified request_id
    user_withdraw.update_one({'_id': ObjectId(request_id)}, {'$set': {'status': 'Done'}})
    return redirect(url_for('withdraw_requests'))


@app.route('/update_deposit_status/<request_id>', methods=['POST'])
def update_deposit_status(request_id):
    # Update the status to 'Done' for the specified request_id
    deposit_request = user_deposit.find_one({'_id': ObjectId(request_id)})
    user_phone = deposit_request['userphonenumber']
    deposit_amount = deposit_request['amount']

    # Update status to 'Done'
    user_deposit.update_one({'_id': ObjectId(request_id)}, {'$set': {'status': 'Done'}})

    # Add the deposit amount to the user's account_balance
    users_collection.update_one({'phonenumber': user_phone}, {'$inc': {'account_balance': int(deposit_amount)}})

    return redirect(url_for('deposit_requests'))


@app.route('/deposit_requests', methods=['GET'])
def deposit_requests():
    # Fetch all deposit requests with 'panding' status
    requests = user_deposit.find({'status': 'panding'})

    return render_template('deposite_req.html', requests=requests)

@app.route('/withdraw_history', methods=['GET'])
def withdraw_history():
    if 'phonenumber' in session:
        user_phone = session['phonenumber']
        withdraw_history = user_withdraw.find({'userphone': user_phone})
        return render_template('withdraw_history.html', withdraw_history=withdraw_history)
    else:
        return redirect(url_for('login'))


app.run(debug=False, host="0.0.0.0", port="8080")