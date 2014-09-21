"""
Options for Messages. Each one looks like:
{type:<'death'|'life'|...>, body:'The world is a teapot and you are the tea.'}
"""

ty_enum = {'death':0, 'hope':1}
d = ty_enum.get('death')
h = ty_enum.get('hope')

options = [
    {'type':d, 'body':'Remember that you are going to die.'},
    {'type':d, 'body':'Death is the destination we all share.'},
    {'type':d, 'body':'Death is very likely the single best invention of life. It clears out the old to make way for the new.'},
    {'type':d, 'body':'Let everything fall away in the face of death. Leave only what is truly important.'},
    {'type':h, 'body':'You are the master of your fate, the captain of your soul.'},
    {'type':h, 'body':'Dare to name the sky your own.'},
    {'type':h, 'body':"For you the flag is flung, for you the bugle trills. For you bouquets and ribbon'd wreaths, for you the shores a-crowding."},
    {'type':h, 'body':'So we beat on, boats against the current, borne back ceaselessly into the past.'},
    {'type':h, 'body':"That is part of the beauty of all literature. You discover that your longings are universal longings, that you're not lonely and isolated from anyone. You belong."},
    {'type':h, 'body':'Let us learn to show our friendship for a man when he is alive and not after he is dead.'}
    ]
