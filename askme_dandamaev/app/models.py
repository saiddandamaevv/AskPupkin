from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q, Subquery, OuterRef, IntegerField

class QuestionManager(models.Manager):
    def with_counts(self):

        return self.get_queryset().annotate(
            answer_count=Count('answer', distinct=True),
            rating=
                Count('questionlike', filter=Q(questionlike__value=1), distinct=True)
             -
                Count('questionlike', filter=Q(questionlike__value=-1), distinct=True)
            
        )

    def new(self):
        return self.with_counts().order_by('-created_at')

    def hot(self):
        return self.with_counts().order_by('-rating')

    def by_tag(self, tag_name):
        return self.with_counts().filter(tags__name=tag_name)

    def get_question_with_answers(self, question_id):
        question = self.with_counts().get(id=question_id)
        answers = Answer.objects.with_counts().filter(question=question)
        return question, answers

class AnswerManager(models.Manager):
    def with_counts(self):
        return self.annotate(
            rating=
                Count('answerlike', filter=Q(answerlike__value=1))
            -
                Count('answerlike', filter=Q(answerlike__value=-1))
        )
    
    def new(self):
        return self.with_counts().order_by('-created_at')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, default='../static/img/gentlemen.jpg')

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    objects = QuestionManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer to {self.question.title}"

LIKES = (
    (1, 'Like'),
    (-1, 'Dislike'),
    (0, 'No Vote')
)

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, db_index=True)
    value = models.SmallIntegerField(choices=LIKES, default=0)

    class Meta:
        unique_together = ['question', 'user']

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=LIKES, default=0)

    class Meta:
        unique_together = ['answer', 'user']