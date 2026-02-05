"""
Management command to seed the database with initial data.
Usage: python manage.py seed
"""
from django.core.management.base import BaseCommand
from encyclopedia.models import Period, Dinosaur, UserProfile
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed database with initial dinosaur and period data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create geological periods
        self.stdout.write('Creating geological periods...')
        triassic, _ = Period.objects.get_or_create(
            name='triassic',
            defaults={
                'era': 'mesozoic',
                'start_mya': 252,
                'end_mya': 201,
                'description': 'The Triassic Period was the first period of the Mesozoic Era. It began after the Permian-Triassic extinction event and ended with the Triassic-Jurassic extinction event. Dinosaurs first appeared during this period.'
            }
        )
        
        jurassic, _ = Period.objects.get_or_create(
            name='jurassic',
            defaults={
                'era': 'mesozoic',
                'start_mya': 201,
                'end_mya': 145,
                'description': 'The Jurassic Period was the middle period of the Mesozoic Era. It was named after the Jura Mountains. This period saw the diversification of dinosaurs including the largest land animals ever to exist.'
            }
        )
        
        cretaceous, _ = Period.objects.get_or_create(
            name='cretaceous',
            defaults={
                'era': 'mesozoic',
                'start_mya': 145,
                'end_mya': 66,
                'description': 'The Cretaceous Period was the last and longest period of the Mesozoic Era. It ended with the Cretaceous-Paleogene extinction event that wiped out all non-avian dinosaurs.'
            }
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Periods created'))
        
        # Create dinosaurs
        self.stdout.write('Creating dinosaurs...')
        
        dinosaurs_data = [
            # Triassic Period
            {
                'name': 'Coelophysis',
                'scientific_name': 'Coelophysis bauri',
                'period': triassic,
                'diet': 'carnivore',
                'length_meters': 3.0,
                'weight_kg': 32.0,
                'description': 'Coelophysis was a small, swift carnivorous dinosaur. It had a long, narrow skull with sharp teeth for catching small prey.',
                'fun_fact': 'Hundreds of Coelophysis fossils were found together at Ghost Ranch, New Mexico, suggesting they may have lived in groups.',
                'discovered_year': 1889
            },
            {
                'name': 'Plateosaurus',
                'scientific_name': 'Plateosaurus engelhardti',
                'period': triassic,
                'diet': 'herbivore',
                'length_meters': 7.0,
                'weight_kg': 4000.0,
                'description': 'Plateosaurus was one of the first large herbivorous dinosaurs. It could walk on two or four legs.',
                'fun_fact': 'Over 100 Plateosaurus skeletons have been found, making it one of the best-known Triassic dinosaurs.',
                'discovered_year': 1837
            },
            {
                'name': 'Eoraptor',
                'scientific_name': 'Eoraptor lunensis',
                'period': triassic,
                'diet': 'omnivore',
                'length_meters': 1.0,
                'weight_kg': 10.0,
                'description': 'Eoraptor is one of the earliest known dinosaurs. It was a small, lightly built animal that walked on two legs.',
                'fun_fact': 'The name "Eoraptor" means "dawn plunderer", reflecting its status as one of the earliest dinosaurs.',
                'discovered_year': 1993
            },
            
            # Jurassic Period
            {
                'name': 'Allosaurus',
                'scientific_name': 'Allosaurus fragilis',
                'period': jurassic,
                'diet': 'carnivore',
                'length_meters': 9.5,
                'weight_kg': 2300.0,
                'description': 'Allosaurus was a large carnivorous dinosaur and one of the apex predators of its time. It had powerful jaws and sharp teeth.',
                'fun_fact': 'Allosaurus could open its jaws extremely wide, possibly to deliver devastating bites to large prey.',
                'discovered_year': 1877
            },
            {
                'name': 'Stegosaurus',
                'scientific_name': 'Stegosaurus stenops',
                'period': jurassic,
                'diet': 'herbivore',
                'length_meters': 9.0,
                'weight_kg': 5000.0,
                'description': 'Stegosaurus is famous for the large plates along its back and the spikes on its tail. It was a large herbivore.',
                'fun_fact': 'Despite its large body, Stegosaurus had a brain the size of a walnut!',
                'discovered_year': 1877
            },
            {
                'name': 'Brachiosaurus',
                'scientific_name': 'Brachiosaurus altithorax',
                'period': jurassic,
                'diet': 'herbivore',
                'length_meters': 25.0,
                'weight_kg': 56000.0,
                'description': 'Brachiosaurus was one of the tallest and largest dinosaurs. It had long front legs and a very long neck.',
                'fun_fact': 'Brachiosaurus could reach vegetation up to 9 meters (30 feet) off the ground!',
                'discovered_year': 1903
            },
            {
                'name': 'Archaeopteryx',
                'scientific_name': 'Archaeopteryx lithographica',
                'period': jurassic,
                'diet': 'carnivore',
                'length_meters': 0.5,
                'weight_kg': 1.0,
                'description': 'Archaeopteryx is considered a transitional fossil between dinosaurs and birds. It had feathers and could possibly fly.',
                'fun_fact': 'Archaeopteryx is often called the "first bird" and provides crucial evidence for the evolution of birds from dinosaurs.',
                'discovered_year': 1861
            },
            
            # Cretaceous Period
            {
                'name': 'Tyrannosaurus Rex',
                'scientific_name': 'Tyrannosaurus rex',
                'period': cretaceous,
                'diet': 'carnivore',
                'length_meters': 12.3,
                'weight_kg': 8400.0,
                'description': 'T. Rex was one of the largest land carnivores of all time. It had massive jaws with teeth up to 30 cm long.',
                'fun_fact': 'T. Rex had the strongest bite force of any land animal ever, estimated at 12,800 pounds!',
                'discovered_year': 1902
            },
            {
                'name': 'Triceratops',
                'scientific_name': 'Triceratops horridus',
                'period': cretaceous,
                'diet': 'herbivore',
                'length_meters': 9.0,
                'weight_kg': 12000.0,
                'description': 'Triceratops had three horns on its face and a large frill protecting its neck. It was a large herbivore.',
                'fun_fact': 'Triceratops means "three-horned face". Its frill may have been used for display and attracting mates.',
                'discovered_year': 1889
            },
            {
                'name': 'Velociraptor',
                'scientific_name': 'Velociraptor mongoliensis',
                'period': cretaceous,
                'diet': 'carnivore',
                'length_meters': 2.0,
                'weight_kg': 15.0,
                'description': 'Velociraptor was a small but deadly predator with a sickle-shaped claw on each foot. It likely hunted in packs.',
                'fun_fact': 'Real Velociraptors were about the size of a turkey, much smaller than shown in movies!',
                'discovered_year': 1924
            },
            {
                'name': 'Spinosaurus',
                'scientific_name': 'Spinosaurus aegyptiacus',
                'period': cretaceous,
                'diet': 'carnivore',
                'length_meters': 15.0,
                'weight_kg': 7400.0,
                'description': 'Spinosaurus is the largest known carnivorous dinosaur. It had a distinctive sail on its back.',
                'fun_fact': 'Spinosaurus was likely semi-aquatic and hunted fish, making it unique among large theropods.',
                'discovered_year': 1912
            },
            {
                'name': 'Ankylosaurus',
                'scientific_name': 'Ankylosaurus magniventris',
                'period': cretaceous,
                'diet': 'herbivore',
                'length_meters': 6.25,
                'weight_kg': 6000.0,
                'description': 'Ankylosaurus was heavily armored with bony plates and had a club-like tail for defense.',
                'fun_fact': 'Ankylosaurus armor was so strong that even T. Rex would have had trouble biting through it!',
                'discovered_year': 1908
            },
            {
                'name': 'Parasaurolophus',
                'scientific_name': 'Parasaurolophus walkeri',
                'period': cretaceous,
                'diet': 'herbivore',
                'length_meters': 10.0,
                'weight_kg': 2500.0,
                'description': 'Parasaurolophus had a distinctive long, curved crest on its head. It was a duck-billed dinosaur.',
                'fun_fact': 'The crest contained nasal passages that may have been used to make loud trumpeting sounds!',
                'discovered_year': 1922
            },
        ]
        
        for dino_data in dinosaurs_data:
            dinosaur, created = Dinosaur.objects.get_or_create(
                name=dino_data['name'],
                defaults=dino_data
            )
            if created:
                self.stdout.write(f'  ✓ Created {dinosaur.name}')
        
        self.stdout.write(self.style.SUCCESS(f'✓ {Dinosaur.objects.count()} dinosaurs in database'))
        
        # Create a test user if needed
        if not User.objects.filter(username='test').exists():
            self.stdout.write('Creating test user...')
            test_user = User.objects.create_user(
                username='test',
                email='test@example.com',
                password='test123'
            )
            UserProfile.objects.create(user=test_user, tokens=100)
            self.stdout.write(self.style.SUCCESS('✓ Test user created (username: test, password: test123)'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write('You can now log in with:')
        self.stdout.write('  Username: test')
        self.stdout.write('  Password: test123')
