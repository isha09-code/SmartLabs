from django.shortcuts import render, redirect, get_object_or_404

from .models import Equipment, Booking, LabBooking

from django.contrib import messages

from datetime import datetime, timedelta





# 🔓 LOGIN

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('user_id')

        password = request.POST.get('password')



        if username and password:

            request.session['student_name'] = username

            return redirect('home')

        else:

            messages.error(request, "Please enter name and password")



    return render(request, 'booking/login.html')





# 🚪 LOGOUT

def logout_view(request):

    request.session.flush()

    return redirect('login')





# 🔄 TIME OVERLAP CHECK

def is_overlap(start1, end1, start2, end2):

    return start1 < end2 and start2 < end1





# 🧪 EQUIPMENT LIST

def equipment_list(request):

    if not request.session.get('student_name'):

        return redirect('login')



    category = request.GET.get('category')



    if category:

        data = Equipment.objects.filter(category=category)

    else:

        data = Equipment.objects.all()



    now = datetime.now()



    for item in data:

        item.lab_blocked = False

        item.free_time = None

        available = item.quantity



        # 🔴 LAB BLOCK CHECK (MINUTES)

        lab_bookings = LabBooking.objects.filter(

            lab=item.category,

            date=now.date()

        )



        for lab in lab_bookings:

            lab_start = datetime.combine(lab.date, lab.time)

            lab_end = lab_start + timedelta(minutes=lab.duration)



            if now < lab_end:

                item.lab_blocked = True

                available = 0

                item.free_time = lab_end.strftime("%I:%M %p")

                break



        # 🔵 EQUIPMENT CHECK (MINUTES)

        if not item.lab_blocked:

            bookings = Booking.objects.filter(

                equipment=item,

                booking_date=now.date()

            )



            total_booked = 0

            latest_end = None



            for b in bookings:

                start = datetime.combine(b.booking_date, b.booking_time)

                end = start + timedelta(minutes=b.duration)



                if now < end:

                    total_booked += b.quantity



                    if not latest_end or end > latest_end:

                        latest_end = end



            if total_booked >= item.quantity:

                available = 0

                if latest_end:

                    item.free_time = latest_end.strftime("%I:%M %p")

            else:

                available = item.quantity - total_booked



        item.available = available



    return render(request, 'booking/equipment.html', {'data': data})





# 📦 BOOK EQUIPMENT

def book_equipment(request, id):

    if not request.session.get('student_name'):

        return redirect('login')



    item = get_object_or_404(Equipment, id=id)

    student_name = request.session.get('student_name', 'Guest')



    if request.method == 'POST':

        name = request.POST.get('name')

        student_class = request.POST.get('student_class')

        roll = request.POST.get('roll')

        pin = request.POST.get('pin')



        date = datetime.strptime(request.POST.get('booking_date'), "%Y-%m-%d").date()

        time = datetime.strptime(request.POST.get('booking_time'), "%H:%M").time()



        duration = int(request.POST.get('duration'))  # ✅ minutes

        quantity = int(request.POST.get('quantity'))

        purpose = request.POST.get('purpose')



        start = datetime.combine(date, time)

        end = start + timedelta(minutes=duration)



        # 🔴 LAB BLOCK CHECK

        lab_bookings = LabBooking.objects.filter(lab=item.category, date=date)



        for lab in lab_bookings:

            lab_start = datetime.combine(lab.date, lab.time)

            lab_end = lab_start + timedelta(minutes=lab.duration)



            if is_overlap(start, end, lab_start, lab_end):

                messages.error(

                    request,

                    f"⛔ Lab booked from {lab.time.strftime('%I:%M %p')} to {lab_end.time().strftime('%I:%M %p')}"

                )

                return render(request, 'booking/book.html', {

                    'item': item,

                    'student_name': student_name

                })



        # 🔵 EQUIPMENT CHECK

        bookings = Booking.objects.filter(

            equipment=item,

            booking_date=date

        )



        total_booked = 0

        latest_end = None



        for b in bookings:

            b_start = datetime.combine(b.booking_date, b.booking_time)

            b_end = b_start + timedelta(minutes=b.duration)



            if is_overlap(start, end, b_start, b_end):

                total_booked += b.quantity



                if not latest_end or b_end > latest_end:

                    latest_end = b_end



        if total_booked + quantity > item.quantity:

            if latest_end:

                messages.error(

                    request,

                    f"❌ Fully booked! Free after {latest_end.time().strftime('%I:%M %p')}"

                )

            else:

                messages.error(request, "❌ Not enough equipment!")



            return render(request, 'booking/book.html', {

                'item': item,

                'student_name': student_name

            })



        # ✅ SAVE

        new_booking = Booking.objects.create(

            equipment=item,

            name=name,

            student_class=student_class,

            roll=roll,

            pin=pin,

            quantity=quantity,

            booking_date=date,

            booking_time=time,

            duration=duration,

            purpose=purpose

        )



        return redirect('booking_success', booking_id=new_booking.pk)



    return render(request, 'booking/book.html', {

        'item': item,

        'student_name': student_name

    })





# ✅ BOOKING SUCCESS

def booking_success(request, booking_id):

    try:

        booking = Booking.objects.get(id=booking_id)

    except Booking.DoesNotExist:

        messages.error(request, "Booking not found.")

        return redirect('home')

    return render(request, 'booking/success.html', {'booking': booking})





# 📜 HISTORY

def booking_history(request):

    if not request.session.get('student_name'):

        return redirect('login')

    bookings = Booking.objects.all().order_by('-booking_date', '-booking_time')

    return render(request, 'booking/history.html', {'bookings': bookings})





# 🏫 LAB BOOKING (MINUTES FIX)

def book_lab(request):

    if not request.session.get('student_name'):

        return redirect('login')



    if request.method == 'POST':

        lab = request.POST.get('lab')

        teacher_name = request.POST.get('teacher_name')



        date = datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()

        time = datetime.strptime(request.POST.get('time'), "%H:%M").time()

        duration = int(request.POST.get('duration'))  # ✅ minutes



        start = datetime.combine(date, time)

        end = start + timedelta(minutes=duration)



        existing = LabBooking.objects.filter(lab=lab, date=date)



        for b in existing:

            b_start = datetime.combine(b.date, b.time)

            b_end = b_start + timedelta(minutes=b.duration)



            if is_overlap(start, end, b_start, b_end):

                messages.error(

                    request,

                    f"❌ Already booked from {b.time.strftime('%I:%M %p')} to {b_end.time().strftime('%I:%M %p')}"

                )

                return render(request, 'booking/book_lab.html')



        new_booking = LabBooking.objects.create(

            lab=lab,

            teacher_name=teacher_name,

            date=date,

            time=time,

            duration=duration

        )



        return redirect('lab_booking_success', id=new_booking.pk)



    return render(request, 'booking/book_lab.html')





# ✅ LAB SUCCESS

def lab_booking_success(request, id):

    try:

        booking = LabBooking.objects.get(id=id)

    except LabBooking.DoesNotExist:

        messages.error(request, "Lab booking not found.")

        return redirect('home')

    return render(request, 'booking/lab_success.html', {'booking': booking})