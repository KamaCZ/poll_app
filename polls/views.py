from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .models import Choice, Question


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Get the selected choice
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # Add a vote to that choice
        selected_choice.votes += 1
        # Save
        selected_choice.save()
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )

    # Redirect to the results page
    return redirect("polls:results", pk=question.id)
