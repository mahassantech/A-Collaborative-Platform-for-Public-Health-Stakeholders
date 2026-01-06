# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.db.models import Count

# from blog.models import BlogPost
# from appointments.models import Appointment
# from .models import Insight


# # @login_required
# # def analyst_dashboard(request):
# #     if request.user.role != "analyst":
# #         return redirect("home")

# #     # 📊 Blog category analysis
# #     category_stats = (
# #         BlogPost.objects
# #         .values("category__name")
# #         .annotate(total=Count("id"))
# #         .order_by("-total")
# #     )

# #     # 📊 Urgency analysis
# #     urgency_stats = (
# #         BlogPost.objects
# #         .values("urgency_level")
# #         .annotate(total=Count("id"))
# #     )

# #     # 📊 Appointment analysis
# #     appointment_stats = (
# #         Appointment.objects
# #         .values("status")
# #         .annotate(total=Count("id"))
# #     )

# #     # 🧠 Simple insight generation (rule based)
# #     generated_insights = []

# #     if category_stats:
# #         top_cat = category_stats[0]
# #         generated_insights.append(
# #             f"{top_cat['category__name']} category-তে সবচেয়ে বেশি blog আছে। এই topic এখন বেশি গুরুত্বপূর্ণ।"
# #         )

# #     for u in urgency_stats:
# #         if u["urgency_level"] == "high" and u["total"] > 5:
# #             generated_insights.append(
# #                 "High urgency blog বেশি দেখা যাচ্ছে, দ্রুত intervention প্রয়োজন।"
# #             )

# #     return render(request, "analytics/dashboard.html", {
# #         "category_stats": category_stats,
# #         "urgency_stats": urgency_stats,
# #         "appointment_stats": appointment_stats,
# #         "generated_insights": generated_insights,
# #     })
