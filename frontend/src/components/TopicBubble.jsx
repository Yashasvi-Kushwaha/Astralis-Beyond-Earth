function TopicBubble({

    title,

    image,

    size = "w-48 h-48",

    onClick

}) {

    return (

        <div

            onClick={onClick}

            className={`
                ${size}
                rounded-full
                relative
                overflow-hidden
                cursor-pointer
                group
                transition-all
                duration-500
                hover:scale-110
                animate-float
            `}
        >

            <img

                src={image}

                className="absolute inset-0 w-full h-full object-cover"

                alt={title}

            />

            <div className="absolute inset-0 bg-black/35 group-hover:bg-black/15 transition"/>

            <div className="absolute inset-0 flex items-center justify-center">

                <h2 className="text-white font-bold text-2xl tracking-widest">

                    {title}

                </h2>

            </div>

        </div>

    );

}

export default TopicBubble;