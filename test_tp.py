import json
import gpts.test_gpt as gpts
import termpaper.utils as tpu
import termpaper.tp as tp

user_message1 = "Mein Themenvorschlag: 'Marginalisierung und Dysmorphia durch Medien – Der " \
                   "Prozess des Othering in alten Medien und neuen Bildungstechnologien' " \
                   "Forschungsleitende Frage: Welche Bedeutung hat es in einer digitalen Gesellschaft, " \
                   "ein positives Imaginäres zu generieren? "

user_message2 = "Hier stellt sich also die Frage nach der didaktischen Qualität digitaler Lernangebote. " \
               "Das wäre für mich eine interessante Frage für die Hausarbeit, allerdings bin ich mir noch" \
               " nicht sicher, ob dafür Forschungsergebnisse und Literatur vorliegen. Auch spannend ist für mich" \
               " die Frage, wie Träger der Erwachsenenbildung mit der zunehmenden Digitalisierung und Mediatisierung " \
               "umgehen. Wie ist der aktuelle Stand? Wie müssen sich Träger der Erwachsenenbildung verändern, " \
               "um Schritt halten zu können und welche Gelingensbedingungen gibt es, " \
               "um mediendidaktische Konzepte erfolgreich umzusetzen?"

user_message3 ="Welche Vor- und Nachteile bietet der Einsatz von Gamification in der dualen " \
               "Berufsausbildung? Welche Vor- und Nachteile bietet der Einsatz von Gamification in " \
               "der Weiterbildung im Bereich XXX? "

user_message4 ="Da mich insbesondere das Vermitteln von Medienkompetenz interessiert und bestehende soziale Ungleichheiten beschäftigen, möchte ich dies gern in Verbindung bringen. Meine Überlegungen zu einem möglichen Thema für die Hausarbeit führt in folgende Richtung: Digitale Ungleichheit an Schulen - innerhalb der Klassen/zwischen den einzelnen Schulformen der Sek. II Welche Chancen bieten digitale Medien im Unterricht, welche Risiken bergen sie? Inwieweit wirkt sich eine fehlende technische Ausstattung in der Schule und Zuhause auf die Nutzung von digitalen Medien aus? - Kompetenz im sozio-moralischen sowie im technischen Bereich Inwieweit erfolgt eine Anleitung durch die Lehrkräfte und die Eltern? Inwieweit führt fehlende (Medien)Kompetenz/fehlendes Wissen zu falscher oder auch Nicht-Nutzung digitaler Medien und/oder des www Inwieweit führt fehlendes ökonomisches und/oder kulturelles Kapital (Fokus auf technische Ausstattung und elterliche Kompetenz)" \
               " zu Reproduktion von (ungleichen) Bildungschancen? Inwieweit wurde diese Problematik durch Corona/Homeschooling verschärft?"


user_message5 ="Mögliche Fragestellungen könnten lauten: 1.  Wie werden Lehrende in Bildungsinstitutionen zu medienkompetenten Lehrkräften aus- oder weitergebildet? " \
               "2.  Welche Maßnahmen ergreifen Universitäten in der Lehramtsausbildung, um Studierende zu medienkompetenten Lehrerinnen und Lehrern zu machen?" \
               " 3. Wie kann gelehrt werden, moralisch gut zu urteilen? Ist es sinnvoll, anhand eines konkreten Projekts die Umsetzung der geforderten Maßnahmen zu überprüfen " \
               "oder zu vergleichen? Sollte der Fokus eher auf einem Teilbereich der Medienkompetenz liegen (z.B. dem Erlernen eines kritischen Urteilsvermögens)? Inwieweit es Material zu direkten Umsetzungsszenarien an Universitäten gibt, fällt mir im Moment schwer einzuschätzen."


def test_process_stu_message():
    response, all_msgs = tp.process_stu_message(user_message2, [])
    print("\n final response: ", response)
    print("\n  all messages: ", all_msgs)


def test_utils():
    # temp = tpu.reference_count() # in all 63 references
    # temp = tpu.get_topics() # list of object
    topics = tpu.get_topic_list()

    temp1 = tpu.find_topics(user_message2, topics)
    # print("\n\ntype of result: ", type(temp1)) # <class 'str'>
    result_1 = json.loads(temp1)
    print("\n\ntype of result: ", type(result_1))  # <class 'list'>
    # print("final result is:", result_1)

    N = 2
    #test_concepts= ["Media Education", "Media and Society", "Media Literacy", "Digital Citizenship", "Media and Technology", "Media Influence"]
    for ele in result_1:
        related_concepts = ele['related_categories']
        result_2 = tpu.find_references(related_concepts)
        refer_N = result_2[:N]
        ele['recommended_references'] = refer_N

    print("final result is:", result_1)


if __name__ == "__main__":
    # test_utils() # worked
    test_process_stu_message()
    print("Everything passed")