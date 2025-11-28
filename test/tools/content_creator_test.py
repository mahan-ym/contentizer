from src.tools.content_creator import look_for_youtube_trends


def test_look_for_youtube_trends_not_none():
    results = look_for_youtube_trends()

    assert results is not None


def test_look_for_youtube_trends_structure():
    results = look_for_youtube_trends()

    assert isinstance(results, list)
    if results:
        first_item = results[0]
        assert "title" in first_item
        assert "description" in first_item
        assert "tags" in first_item
        assert "publishedAt" in first_item
        assert "channel" in first_item
        assert "views" in first_item
        assert "likes" in first_item
        assert "comments" in first_item
