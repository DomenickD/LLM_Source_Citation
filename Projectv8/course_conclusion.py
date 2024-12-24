"""The final page of the course."""

import streamlit as st


def course_conclusion():
    """Render the course conclusion page."""
    st.title("Course Conclusion")
    st.caption("We made it!!")

    # Adding content from the DOCX file
    st.subheader("Acknowledgements")
    st.markdown(
        """
    **FOR BRETT AND ALL HE HAS DONE FOR US**
    """
    )

    acknowledgements = {
        "Maggie Hylan": """My name is Margaret Hylan and I was on Brett's \
        DS team as an RA. Brett was an exceptional mentor who went above\
        and beyond for us. When I first started the program I did not \
        know anything about Python and Brett always took the time to \
        answer my (very long) messages and answer my calls. \
        Additionally, I struggled with transitioning from an academic \
        space where I was given a grade to a professional space where \
        my work was either satisfactory or not. Brett's patience and \
        willingness to guide me made the transition much easier. \
        I am extremely grateful for all the work and time that \
        he has dedicated to us.""",
        "Domenick (Dobby) Dobbs": """My name is Domenick, but everyone's\
        called me Dobby since my army days. From the get-go, \
        Brett had this incredible ability to meet me right \
        where I was at, skill-wise. He challenged me, for \
        sure, but always balanced it with teaching me new \
        coding techniques and problem-solving strategies.
        \nOur weekly meetings were a cornerstone, but Brett's \
        dedication went beyond that. We'd often connect \
        outside of those scheduled times, and no matter \
        how packed his schedule was, he always found time \
        to guide me through those inevitable coding roadblocks. \
        But here's the thing: he didn't just hand me solutions. \
        He taught me to be thorough, to explore every possible avenue \
        before settling on the easy way out. He called it the \
        "No Free Lunch Theorem," and it's something I'll carry with me.
        \nBrett was also incredibly attuned to the needs of his students. \
        He'd often break down particularly challenging weeks into \
        multi-week deep dives, which made grasping those complex topics \
        so much easier. It was clear that he put a ton of thought into \
        each and every meeting, ensuring that all of us RAs had the \
        opportunity to learn something new and be challenged in a \
        way that fostered real growth.
        \nI have immense respect for Brett and everything he taught us. \
        His dedication to us was unmatched. Honestly, \
        he is the real deal - 10/10!""",
        "Julio Figueroa": """Working with Brett Waugh in the Data \
            Science RA program has been an incredible experience. \
        Brett has a unique way of leading—he challenges you to think \
        deeply and pushes you to grow while providing just enough \
        guidance to keep you on track. He never simply gave us \
        answers but instead pointed us to the right resources, \
        encouraging us to dig deeper and develop our skills. \
        Even when our schedules were chaotic, Brett remained \
        calm and collected, always making time to offer extra \
        guidance outside of meetings.
        \nWhat stood out the most was his ability to motivate and \
        inspire without micromanaging. He created a perfect \
        balance between fostering independence and encouraging \
        collaboration. Brett's feedback was always constructive, \
        helping us improve without ever diminishing our efforts. \
        For me, this was one of the few times I've truly looked \
        up to someone younger than myself—a testament to his \
        leadership and wisdom. His mentorship left a lasting \
        impact, and I feel incredibly fortunate to have learned \
        under his guidance.""",
        "Chad Lutz": """Brett put together an excellent program \
            for the Research Assistant participants. The content was \
        relevant, challenging, and structured to set us up for \
        success. Although my participation was limited to the first \
        semester, the experience was crucial in securing my data \
        science position at SOCOM and has contributed significantly \
        to my success in the role. Brett demonstrated a deep \
        understanding of the material, exhibited patience with \
        the students, and consistently motivated us to stay engaged.""",
        "Daniel Loehnert": """Brett did a phenomenal job with \
            the internship while I was attending. I personally \
        really appreciated how flexible he was with my crazy \
        schedule along with what the other interns were juggling\
        as well. The IEX internship was definitely challenging, \
        but Brett was available to answer any questions that I \
        had or that the team had. I give a huge shout out to \
        Brett for everything that he did for the internship and \
        how much instruction he gave us throughout the internship. \
        Thank you, Brett, for your help and everything you did! \
        Keep up the drive and continue doing great things""",
        "Luke Wilson": """Brett Waugh has been an outstanding \
        mentor and teacher for me during the course of the data \
        science internship. Not only did he design the entire \
        curriculum, he also worked with us to make the curriculum \
        interesting and applicable to the real world, making the \
        entire program feel that much more worthwhile. He was \
        exceptionally liberal with his time, meeting with us \
        whenever he could, and helping us in any way possible. \
        He worked around our schedules even though his schedule \
        was probably busier than ours, and made sure that everyone\
         was caught up, and didn't fall behind. I learned an \
        extraordinary amount about python, statistics, \
        machine learning, and how to create apps to display results. \
        My expectations of this program were blown out of the \
        water, because of Brett and how well he led this program. \
        Even when we finished the planned curriculum, Brett \
        worked with us to develop new projects that were \
        interesting, and worthwhile, even going so far as \
        to use some of his personal resources to make sure \
        we were adequately challenged.""",
    }

    for name, text in acknowledgements.items():
        st.markdown(f"### {name}")
        st.markdown(text)
