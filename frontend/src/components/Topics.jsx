import { useState } from "react";
import { useNavigate } from "react-router-dom";

import TopicBubble from "./TopicBubble";
import TopicModal from "./TopicModal";

import cosmos from "../assets/topics/cosmos.jpg";
import stars from "../assets/topics/stars.jpg";
import planets from "../assets/topics/planets.jpg";
import nebula from "../assets/topics/nebula.jpg";
import multiverse from "../assets/topics/multiverse.jpg";

function Topics() {

    const navigate = useNavigate();

    const [selectedTopic, setSelectedTopic] = useState(null);

    const topics = [

        {
            title: "Cosmos",
            image: cosmos,
            definition:
                "The cosmos is the entire universe, including all galaxies, stars, planets, matter, energy, space and time.",

            fact:
                "The observable universe is about 93 billion light-years across."
        },

        {
            title: "Stars",
            image: stars,
            definition:
                "Stars are massive luminous spheres of plasma powered by nuclear fusion.",

            fact:
                "Our Sun is one of roughly 200 billion stars in the Milky Way."
        },

        {
            title: "Planets",
            image: planets,
            definition:
                "Planets are celestial bodies that orbit a star and are massive enough to become nearly spherical.",

            fact:
                "Jupiter contains more than twice the mass of all the other planets combined."
        },

        {
            title: "Nebula",
            image: nebula,
            definition:
                "A nebula is a giant cloud of gas and dust where many new stars are born.",

            fact:
                "The Eagle Nebula contains the famous Pillars of Creation."
        },

        {
            title: "Multiverse",
            image: multiverse,
            definition:
                "The multiverse is a hypothetical collection of multiple universes beyond our own.",

            fact:
                "There is currently no direct observational evidence that the multiverse exists."
        }

    ];

    return (

        <>

            <section className="mt-36 mb-28">

                <h2 className="text-center text-5xl font-light mb-20">

                    Explore Space

                </h2>

                <div className="flex flex-wrap justify-center gap-14">

                    {topics.map((topic) => (

                        <TopicBubble
                            key={topic.title}
                            title={topic.title.toUpperCase()}
                            image={topic.image}
                            onClick={() => setSelectedTopic(topic)}
                        />

                    ))}

                </div>

            </section>

            <TopicModal

                topic={selectedTopic}

                onClose={() => setSelectedTopic(null)}

                onAsk={(title) =>

                    navigate("/chat", {

                        state: {

                            question: `Tell me about ${title}`

                        }

                    })

                }

            />

        </>

    );

}

export default Topics;