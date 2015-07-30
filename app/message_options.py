"""
Options for Messages. Each one looks like:
{type:<'death'|'life'|...>, body:'The world is a teapot and you are the tea.'}
"""

ty_enum = {'death':0, 'hope':1, 'intro':2, 'reintro':3, 'growth':4}
d = ty_enum.get('death')
h = ty_enum.get('hope')
i = ty_enum.get('intro')
r = ty_enum.get('reintro')
g = ty_enum.get('growth')

options = [
    {'type':i, 'body':"Hi, we're so glad to send you hints of hope. You'll receive them every one to two weeks, and if you decide you no longer need hope, reply HOPE to this number."},
    {'type':d, 'body':'Remember that you are going to die.'},
    {'type':d, 'body':'Death is the destination we all share.'},
    {'type':d, 'body':'Death is very likely the single best invention of life. It clears out the old to make way for the new.'},
    {'type':d, 'body':'Let everything fall away in the face of death. Leave only what is truly important.'},
    {'type':d, 'body':'Let us beware of saying that death is the opposite of life. The living being is only a species of the dead, and a very rare species.'},
    {'type':d, 'body':'All that you see will soon perish; those who witness this perishing will soon perish themselves. Die in extreme old age or die before your time - it will all be the same.'},
    {'type':d, 'body':'Whenever someone tells me he dreamed, I wonder if he realizes that he has never done anything but dream.'},
    {'type':d, 'body':'Regardless, the outcome is the same: we are all going to die.'},
    {'type':d, 'body':"This is your life and it's ending one moment at a time."},
    {'type':d, 'body':'You are the music while the music lasts.'},
    {'type':h, 'body':'You are the master of your fate, the captain of your soul.'},
    {'type':h, 'body':'Dare to name the sky your own.'},
    {'type':h, 'body':"For you the flag is flung, for you the bugle trills. For you bouquets and ribbon'd wreaths, for you the shores a-crowding."},
    {'type':d, 'body':'So we beat on, boats against the current, borne back ceaselessly into the past.'},
    {'type':h, 'body':"That is part of the beauty of all literature. You discover that your longings are universal longings, that you're not lonely and isolated from anyone. You belong."},
    {'type':h, 'body':'Let us learn to show our friendship for a man when he is alive and not after he is dead.'},
    {'type':h, 'body':'Set your goals high; Make friends with different kinds of people; Enjoy simple pleasures'},
    {'type':h, 'body':'Stand on high ground; Sit on level ground; Walk on expansive ground.'},
    {'type':h, 'body':"Still, I'll rise"},
    {'type':r, 'body':"Hi there, welcome back to Hints of Hope. We're so honored to be your Mercury of inspiration."},
    {'type':d, 'body':"The race for quality has no finish line, so technically, it's more like a death march."},
    {'type':h, 'body':"Trust yourself. You know more than you think you do."},
    {'type':h, 'body':"Rise up. Start Fresh. See the bright opportunity in each day."},
    {'type':h, 'body':"Destiny dressed you this morning my friend, and now Fear is trying to pull off your pants. If you give up, if you give in, you're gonna end up naked with Fear just standing there laughing at your dangling unmentionables!"},
    {'type':d, 'body':"Things are sweeter when they're lost. I know - because once I wanted something and got it. It was the only thing I ever wanted badly. And when I got it, it turned to dust in my hands."},
    {'type':h, 'body':"Her heart sank into her shoes as she realized at last how much she wanted him. No matter what his past was, no matter what he had done. Which was not to say that she would ever let him know, but only that he moved her chemically more than anyone she had ever met, that all other men seemed pale beside him."},
    {'type':h, 'body':"Somewhere inside of you will always be the person that you were in your finest hour."},
    {'type':h, 'body':"You are the finest, loveliest, tenderest, and most beautiful person someone has ever known - and even that is an understatement."},
    {'type':d, 'body':"There are all kinds of love in this world, but never the same love twice."},
    {'type':h, 'body':"Listen to the mustn'ts, child. Listen to the don'ts. Listen to the shouldn'ts, the impossibles, the won'ts. Listen to the never haves, then listen close to me... Anything can happen, child. Anything can be."},
    {'type':d, 'body':"If you're reading this...Congratulations, you're alive. If that's not something to smile about, then I don't know what is."},
    {'type':d, 'body':"The deepest regret is death. The only thing to face is death. This is all I think about. There's only one issue here. I want to live."},
    {'type':d, 'body':"Your status as a doomed man lends your words a certain prestige and authority. As the time nears, people will be eager to hear what you have to say. They will seek you out."},
    {'type':h, 'body':"If you're going through hell, keep going."},
    {'type':h, 'body':"Be the person your dog thinks you are."},
    {'type':h, 'body':"Just do it."},
    {'type':d, 'body':"Coffee should not involve whipped cream or sweet syrups. It should be a black, bitter foretaste of the day that is to come."},
    {'type':d, 'body':"You still die alone."},
    {'type':d, 'body':"Stop. Look around you. In ten years, who will be left? Twenty years? Fifty?"},
    {'type':h, 'body':"The world is yours for the making. Mold your future as you see fit."},
    {'type':h, 'body':"I kept my head down. I jumped into a little creek, which became a river, which turned into a gulf, which grew into an ocean. All I ever did was swim."},
    {'type':h, 'body':"If you want to make art, make art. Do not wait for an institution to give you permission."},
    {'type':d, 'body':"Not answering email is important to remind us that life will go on without us."},
    {'type':d, 'body':"When life hands you lemons, accept that the universe is indifferent to your pain."},
    {'type':h, 'body':"Greatly he failed, but he did dare greatly."},
    {'type':d, 'body':"When that tomorrow comes, you're going to want one more today."},
    {'type':d, 'body':"As you find yourself adventuring through unknown lands, check your engine temperature frequently."},
    {'type':h, 'body':"Immortality is to live your life doing good things and leaving your mark behind."},
    {'type':d, 'body':"How many times will you watch the full moon rise? Perhaps twenty. And yet it all seems limitless."},
    {'type':d, 'body':"Because we don't know when we will die, we get to think of life as an inexhaustible well. Yet everything happens a certain number of times, and a very small number, really."},
    {'type':h, 'body':"I do not wish to say that one should love death; but one should love life so magnanimously, so without calculating and selecting, that love of death is continually and involuntarily included."},
    {'type':h, 'body':"You will be a happy moment in someone's life."},
    {'type':d, 'body':"Lost time is never found again. Do it now."},
    {'type':d, 'body':"Today is difficult, tomorrow is much more difficult, the day after tomorrow is very beautiful, but most die tomorrow evening."},
    {'type':g, 'body':'Help your friends and loved ones by sending them a Hint of Hope @ hintofhope.today!\n(or reply to this message with their phone number)'},
    ]
