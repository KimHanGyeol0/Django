from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    tags = post.hashtags.all()
    content = post.content
    content_list = content.split()
    for tag in tags:
        for i in range(len(content_list)):
            if tag.content == content_list[i]:
                content_list[i] = f'<a href="/posts/hashtags/{tag.pk}">{tag.content}</a>'
    content = ' '.join(content_list)

    # for tag in tags:
    #     content = content.replace(tag.content, f'<a href="/posts/hashtags/{tag.pk}">{tag.content}</a>')

    return content