import boto3
from datetime import datetime
import time

ec2 = boto3.client('ec2', region_name='ap-south-1')

VOLUME_ID = 'vol-0536085b80fcdd726'

def create_snapshot():
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=f"Automated snapshot {datetime.now()}"
    )
    print("Created:", response['SnapshotId'])
    time.sleep(20)

def delete_old_snapshots():
    snapshots = ec2.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}],
        OwnerIds=['self']
    )['Snapshots']

    snapshots = sorted(snapshots, key=lambda x: x['StartTime'], reverse=True)

    print("Total snapshots:", len(snapshots))

    for snap in snapshots[5:]:
        print("Deleting:", snap['SnapshotId'])
        ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])

if __name__ == "__main__":
    create_snapshot()
    delete_old_snapshots()