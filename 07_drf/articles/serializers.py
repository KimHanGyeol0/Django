from rest_framework import serializers
from .models import Article, Comment

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta():
        model = Article
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Comment
        fields = '__all__'
        # 이 article 사용자가 직접 변경하는게 아니다, 코드가 변경하는 것이다
        read_only_fields = ('article',)

class ArticleSerializer(serializers.ModelSerializer):
    # 게시물과 댓글도 같이 보여줘야함
    # 게시물에 달린 댓글 id만 출력, 수정하는 것이 아니니까 read_only=True
    # comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 게시물에 달린 댓글 json을 리스트로 가져옴
    comment_set = CommentSerializer(many=True, read_only=True)
    # 몇 개 달렸는지
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    class Meta():
        model = Article
        fields = '__all__'
