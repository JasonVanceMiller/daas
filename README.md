# Goal: 

The goal of this project, is to take a small subset of wikipedia, and insert it into Opensearch with the goal of doing both NLQ and traditional search to get document ids out. 

You can run each of these commands in vim. Highlight with V, and run with :w !bash

# Setup OS in Docker:

docker pull opensearchproject/opensearch:latest

docker run -dit --rm -p 9201:9200 -p 9601:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=ChangeIt123!" --name opensearch_c opensearchproject/opensearch:latest

# Test connectivity:

curl -XGET -ku 'admin:ChangeIt123!' https://localhost:9201/_cluster/health

If you see a json blurb, then that means you did a good job!

# Initalizing OS:

## Cleanup index (if it already exists):

curl -XDELETE -ku 'admin:ChangeIt123!' https://localhost:9201/wiki
    
## Create index:

curl -XPUT -ku 'admin:ChangeIt123!' https://localhost:9201/wiki -H 'Content-Type: application/json' -d ' {
    "settings": {
        "index.knn": true
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "tags": {
                "type": "keyword"
            },
            "paragraph": {
                "type": "text"
            },
            "embedding": {
                "type": "knn_vector",
                "dimension": 512,
                "space_type": "l2"
            },
            "embedding_model": {
                "type": "keyword"
            },
            "paragraph_number": {
                "type": "integer"
            },
            "version": {
                "type": "keyword"
            }
        }
    }
}'

# Index data:

./transformer.py

Transformer.py goes through all of the wikipedia sample documents, splits them into individual paragraphs, and inserts them as described in the mapping (minus tag). The embeddings are done with: "https://tfhub.dev/google/universal-sentence-encoder/4"

You can see all of the documents that got indexed. They are in documents.txt. This is useful if you expect something to show up, but it doesn't.

# Search:

## Curl:

curl -ku 'admin:ChangeIt123!' https://localhost:9201/wiki/_search -H "Content-Type: application/json" -d "{\"query\": {\"match\":{\"paragraph\": {\"query\": \"Michael Jackson\"}}}}"

## Python:

./search.py --nlq         'Michael Jackson'
./search.py --traditional 'Michael Jackson'

# Results:

## NLQ Favorable:
./search.py --nlq         'Michael Jackson'

####################
Michael Jackson
Michael Joseph Jackson (August 29, 1958 – June 25, 2009) was an American singer, songwriter, dancer, and philanthropist. Dubbed the "King of Pop", he is regarded as one of the most culturally significant figures of the 20th century. Over a four-decade career, his music achievements broke racial barriers in America and made him a dominant figure across the world. Through songs, stages, and fashion, he proliferated visual performance for artists in popular music; popularizing street dance moves including the moonwalk, the robot, and the anti-gravity lean. Jackson is often deemed the greatest entertainer of all time based on his acclaim and records.[1]

####################
Michael Jackson
The success transformed Jackson into a dominant force in global pop culture,[88] and the album "conquered racial divides".[89] Jackson had the highest royalty rate in the music industry at that point, with about $2 for every album sold (equivalent to $6 in 2024), and was making record-breaking profits. Dolls modeled after Jackson appeared in stores in May 1984 for $12 each.[90] In the same year, The Making of Michael Jackson's Thriller, a documentary about the music video, won a Grammy for Best Music Video (Longform).[61] Time described Jackson's influence at that point as "star of records, radio, rock video. A one-man rescue team for the music business. A songwriter who sets the beat for a decade. A dancer with the fanciest feet on the street. A singer who cuts across all boundaries of taste and style and color too."[90] The New York Times wrote "in the world of pop music, there is Michael Jackson and there is everybody else".[91]

####################
Michael Jackson
Later in 2014, Queen released a duet recorded with Jackson in the 1980s.[67] A compilation album, Scream, was released on September 29, 2017.[395] A jukebox musical, MJ the Musical, premiered on Broadway in 2022.[396] Myles Frost won the 2022 Tony Award for Best Actor in a Musical for his portrayal of Jackson.[397] On November 18, 2022, Epic released a 40th-anniversary edition reissue of Thriller.[398][399] A biographical film based on Jackson's life, Michael, directed by Antoine Fuqua, is scheduled for October 2025.[400] Jackson is played by his nephew Jaafar Jackson. Deadline Hollywood reported that the film "will not shy away from the controversies of Jackson's life".[401] Since Jackson's death, his estate has grossed $2 billion in ticket revenue from MJ the Musical, Michael Jackson's This Is It and two Cirque du Soleil productions.[402]

####################
Michael Jackson
Jackson's posthumous releases and productions are administered by the estate of Michael Jackson, which owns Jackson's trademarks and rights to his name, image and likeness.[376] The first posthumous Jackson song, "This Is It", co-written in the 1980s with Paul Anka, was released in October 2009. The surviving Jackson brothers reunited to record backing vocals.[377] It was followed by a documentary film about the rehearsals for the canceled This Is It tour, Michael Jackson's This Is It,[378] and a compilation album.[379] Despite a limited two-week engagement, the film became the highest-grossing documentary or concert film ever, with earnings of more than $260 million worldwide.[380] Jackson's estate received 90% of the profits.[381] In late 2010, Sony released the first posthumous album, Michael, and the lead single "Hold My Hand", a duet with Akon. The Jackson collaborator will.i.am expressed disgust, saying that Jackson would not have approved the release.[382]

## Traditional Search Favorable:
./search.py --traditional 'Michael Jackson'

####################
Michael Jackson
Michael Joseph Jackson Jr. (commonly known as Prince) was born on February 13, 1997. His sister Paris-Michael Katherine Jackson was born on April 3, 1998.[252] Jackson and Rowe divorced in 2000, Rowe conceded custody of the children, with an $8 million settlement (equivalent to $15.1 million in 2024).[253] In 2004, after the second child abuse allegations against Jackson, she returned to court to reclaim custody. The suit was settled in 2006.[254]

####################
Michael Jackson
Documentaries such as Square One: Michael Jackson, Neverland Firsthand: Investigating the Michael Jackson Documentary and Michael Jackson: Chase the Truth, presented information countering the claims suggested by Leaving Neverland.[426][427][428] Jackson's album sales increased following the documentary screenings.[429] Billboard senior editor Gail Mitchell said she and a colleague interviewed about thirty music executives who believed Jackson's legacy could withstand the controversy.[430] In late 2019, some New Zealand and Canadian radio stations re-added Jackson's music to their playlists, citing "positive listener survey results".[431][432]

####################
Michael Jackson
In October 2011, the theater company Cirque du Soleil launched Michael Jackson: The Immortal World Tour, a $57-million production,[387] in Montreal, with a permanent show resident in Las Vegas.[388] A larger and more theatrical Cirque show, Michael Jackson: One, designed for residency at the Mandalay Bay resort in Las Vegas, opened on May 23, 2013, in a renovated theater.[389][390]

####################
Michael Jackson
Jackson's posthumous releases and productions are administered by the estate of Michael Jackson, which owns Jackson's trademarks and rights to his name, image and likeness.[376] The first posthumous Jackson song, "This Is It", co-written in the 1980s with Paul Anka, was released in October 2009. The surviving Jackson brothers reunited to record backing vocals.[377] It was followed by a documentary film about the rehearsals for the canceled This Is It tour, Michael Jackson's This Is It,[378] and a compilation album.[379] Despite a limited two-week engagement, the film became the highest-grossing documentary or concert film ever, with earnings of more than $260 million worldwide.[380] Jackson's estate received 90% of the profits.[381] In late 2010, Sony released the first posthumous album, Michael, and the lead single "Hold My Hand", a duet with Akon. The Jackson collaborator will.i.am expressed disgust, saying that Jackson would not have approved the release.[382]

## NLQ Neutral:
./search.py --nlq 'Batman'

####################
Bat
Rhinopomatidae (mouse-tailed bats) 

####################
Bat
Natalidae (funnel-eared bats) 

####################
Bat
Myzopodidae (sucker-footed bats)

####################
Bat
Molossidae (free-tailed bats) 

## Traditional Neutral:
./search.py --traditional 'Batman'

####################
Amazon (company)
On October 18, 2011, Amazon.com announced a partnership with DC Comics for the exclusive digital rights to many popular comics, including Superman, Batman, Green Lantern, Sandman, and Watchmen. The partnership has caused well-known bookstores like Barnes & Noble to remove these titles from their shelves.[72]

####################
Bat
The Weird Sisters in Shakespeare's Macbeth used the fur of a bat in their brew.[285] In Western culture, the bat is often a symbol of the night and its foreboding nature. The bat is a primary animal associated with fictional characters of the night, both villainous vampires, such as Count Dracula and before him Varney the Vampire,[286] and heroes, such as the DC Comics character Batman.[287] Kenneth Oppel's Silverwing novels narrate the adventures of a young bat,[288] based on the silver-haired bat of North America.[289]

####################
Mariah Carey
Carey's life and career have received widespread media coverage. She has been dubbed the "Queen of Christmas" due to the enduring popularity of her holiday music, particularly Merry Christmas (1994), one of the best-selling holiday albums, and its single "All I Want for Christmas Is You", which is one of the best selling singles of all time. Outside of music, she co-founded Camp Mariah with the Fresh Air Fund in 1994; starred in films such as Precious (2009), The Butler (2013), and The Lego Batman Movie (2017); and served as a judge on American Idol (2013). Her 2020 memoir, The Meaning of Mariah Carey, reached number one on The New York Times Best Seller list.

####################
Video game
Separately, video games are also frequently used as part of the promotion and marketing for other media, such as for films, anime, and comics. However, these licensed games in the 1990s and 2000s often had a reputation for poor quality, developed without any input from the intellectual property rights owners, and several of them are considered among lists of games with notably negative reception, such as Superman 64. More recently, with these licensed games being developed by triple-A studios or through studios directly connected to the licensed property owner, there has been a significant improvement in the quality of these games, with an early trendsetting example of Batman: Arkham Asylum.[118]


## NLQ Adversarial:
./search.py --nlq 'Disney'

####################
Eukaryote
Holozoa (inc. animals) 

####################
Frog
Calyptocephalellidae

####################
Michael Jackson
Jackson worked with George Lucas and Francis Ford Coppola on the 17-minute $30 million 3D film Captain EO, which ran from 1986 at Disneyland and Epcot, and later at Tokyo Disneyland and Euro Disneyland.[131] After having been removed in the late 1990s, it returned to the theme park for several years after Jackson's death.[132] In 1987, Ebony reported that Jackson had disassociated himself from the Jehovah's Witnesses.[133] Katherine Jackson said this might have been because some Witnesses strongly opposed the Thriller video,[134] which Michael denounced in a Witness publication in 1984.[135] In 2001, Jackson told an interviewer he was still a Jehovah's Witness.[136]

####################
Insect
Protura (coneheads) 

## Traditional Adversarial:
./search.py --traditional 'Disney'

####################
The Beatles
On 8 May 2024, the 1970 film Let It Be was released on Disney+, following a digital restoration by Jackson's Park Road Post; it was the first time it was publicly screened since its original theatrical release.[394]

####################
YouTube
On February 28, 2017, in a press announcement held at YouTube Space Los Angeles, YouTube announced YouTube TV, an over-the-top MVPD-style subscription service that would be available for United States customers at a price of US$65 per month. Initially launching in five major markets (New York City, Los Angeles, Chicago, Philadelphia and San Francisco) on April 5, 2017,[195][196] the service offers live streams of programming from the five major broadcast networks (ABC, CBS, The CW, Fox and NBC, along with selected MyNetworkTV affiliates and independent stations in certain markets), as well as approximately 60 cable channels owned by companies such as The Walt Disney Company, Paramount Global, Fox Corporation, NBCUniversal, Allen Media Group and Warner Bros. Discovery (including among others Bravo, USA Network, Syfy, Disney Channel, CNN, Cartoon Network, E!, Fox Sports 1, Freeform, FX and ESPN).[197][198]

####################
The Beatles
McCartney filed suit for the dissolution of the Beatles' contractual partnership on 31 December 1970.[308] Legal disputes continued long after their break-up and the dissolution was not formalised until 29 December 1974,[309] when Lennon signed the paperwork terminating the partnership while on vacation with his family at Walt Disney World Resort in Florida.[310]

####################
The Beatles
In November 2021, The Beatles: Get Back, a documentary directed by Peter Jackson using footage captured for the Let It Be film, was released on Disney+ as a three-part miniseries.[380] A book by the same title was released on 12 October.[381] A super deluxe version of the Let It Be album was released on 15 October.[382] In January 2022, the album Get Back (Rooftop Performance), consisting of newly mixed audio of the Beatles' rooftop performance, was released on streaming services.[383]

# Conclusion:

Obviously, LLMs are very power and a 3 hour test isn't a fair judgement, but we can make some preliminary conclusions. It looks like nlq did a better job on the Michael Jackson test, where traditional bumped Michael Jackson jr to the top. For the neutral test, traditional search was able to find paragraphs where Batman made a minor appearance, while nlq focused more on actual bats, which is a clear victory for traditional search, and is probably representative of the experience for developer documentation (like searching for function names). In the adversarial case, nlq flailed around and returned species of bugs and frogs, while traditional search at least found disney+ consistently, which would be the first breadcrumb back to the disney page. Opensearch has some min distance and max distance parameters, so maybe the biology results could be filtered out.

To conclude, I am pretty disappointed with NLQ's performance. It gets pretty mixed up by the fungi, birds, frogs, and insect tables when it struggles to find a match, and focuses mostly on the majority content of the paragraph. This is especially concerning for finding function usage in code snippets. 

If I were a developer, I would prefer traditional search significantly more. 

# Misc:
curl -ku 'admin:ChangeIt123!' https://localhost:9201/wiki/_search -H "Content-Type: application/json" -d "{\"query\": {\"match_all\":{}},\"size\":10000,\"_source\": [\"title\"]}"
